package com.acqinc.mcbridge;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public final class AcqMinecraftBridge implements ModInitializer {
    private static final int PORT = 18765;
    private static volatile MinecraftServer server;
    private static HttpServer http;

    @Override
    public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(s -> {
            server = s;
            try {
                startHttp();
                System.out.println("[Acq Minecraft Bridge] listening on http://127.0.0.1:" + PORT);
            } catch (IOException e) {
                throw new RuntimeException("Unable to start Acq Minecraft Bridge", e);
            }
        });
        ServerLifecycleEvents.SERVER_STOPPING.register(s -> {
            server = null;
            if (http != null) {
                http.stop(0);
                http = null;
            }
        });
    }

    private static synchronized void startHttp() throws IOException {
        if (http != null) return;
        http = HttpServer.create(new InetSocketAddress("127.0.0.1", PORT), 0);
        http.createContext("/health", AcqMinecraftBridge::health);
        http.createContext("/setblock", AcqMinecraftBridge::setBlock);
        http.createContext("/fill", AcqMinecraftBridge::fill);
        http.createContext("/query", AcqMinecraftBridge::query);
        http.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
        http.start();
    }

    private static void health(HttpExchange ex) throws IOException {
        if (!"GET".equalsIgnoreCase(ex.getRequestMethod())) {
            reply(ex, 405, "{\"ok\":false,\"error\":\"GET required\"}");
            return;
        }
        MinecraftServer s = server;
        if (s == null) {
            reply(ex, 503, "{\"ok\":false,\"ready\":false}");
            return;
        }
        String world = jsonEscape(s.getWorldData().getLevelName());
        reply(ex, 200, "{\"ok\":true,\"ready\":true,\"world\":\"" + world + "\"}");
    }

    private static void setBlock(HttpExchange ex) throws IOException {
        if (!"POST".equalsIgnoreCase(ex.getRequestMethod())) {
            reply(ex, 405, "{\"ok\":false,\"error\":\"POST required\"}");
            return;
        }
        String[] p = body(ex).trim().split("\\s+");
        if (p.length != 4) {
            reply(ex, 400, "{\"ok\":false,\"error\":\"body: x y z minecraft:block\"}");
            return;
        }
        try {
            int x = Integer.parseInt(p[0]), y = Integer.parseInt(p[1]), z = Integer.parseInt(p[2]);
            BlockState state = resolveBlock(p[3]);
            boolean changed = onServer(() -> level().setBlockAndUpdate(new BlockPos(x,y,z), state));
            reply(ex, 200, "{\"ok\":true,\"changed\":" + changed + "}");
        } catch (Exception e) {
            reply(ex, 400, errorJson(e));
        }
    }

    private static void fill(HttpExchange ex) throws IOException {
        if (!"POST".equalsIgnoreCase(ex.getRequestMethod())) {
            reply(ex, 405, "{\"ok\":false,\"error\":\"POST required\"}");
            return;
        }
        String[] p = body(ex).trim().split("\\s+");
        if (p.length != 7) {
            reply(ex, 400, "{\"ok\":false,\"error\":\"body: x1 y1 z1 x2 y2 z2 minecraft:block\"}");
            return;
        }
        try {
            int x1=Integer.parseInt(p[0]), y1=Integer.parseInt(p[1]), z1=Integer.parseInt(p[2]);
            int x2=Integer.parseInt(p[3]), y2=Integer.parseInt(p[4]), z2=Integer.parseInt(p[5]);
            BlockState state = resolveBlock(p[6]);
            long volume=(long)(Math.abs(x2-x1)+1)*(Math.abs(y2-y1)+1)*(Math.abs(z2-z1)+1);
            if (volume > 100_000L) throw new IllegalArgumentException("fill volume exceeds 100000 blocks");
            int changed=onServer(() -> {
                ServerLevel level=level();
                int count=0;
                for(int y=Math.min(y1,y2);y<=Math.max(y1,y2);y++)
                    for(int z=Math.min(z1,z2);z<=Math.max(z1,z2);z++)
                        for(int x=Math.min(x1,x2);x<=Math.max(x1,x2);x++)
                            if(level.setBlockAndUpdate(new BlockPos(x,y,z),state)) count++;
                return count;
            });
            reply(ex,200,"{\"ok\":true,\"changed\":"+changed+",\"volume\":"+volume+"}");
        } catch(Exception e) {
            reply(ex,400,errorJson(e));
        }
    }

    private static void query(HttpExchange ex) throws IOException {
        if (!"POST".equalsIgnoreCase(ex.getRequestMethod())) {
            reply(ex,405,"{\"ok\":false,\"error\":\"POST required\"}");
            return;
        }
        String[] p=body(ex).trim().split("\\s+");
        if(p.length!=3) {
            reply(ex,400,"{\"ok\":false,\"error\":\"body: x y z\"}");
            return;
        }
        try {
            int x=Integer.parseInt(p[0]), y=Integer.parseInt(p[1]), z=Integer.parseInt(p[2]);
            String result=onServer(() -> {
                BlockState state=level().getBlockState(new BlockPos(x,y,z));
                var key=BuiltInRegistries.BLOCK.getKey(state.getBlock());
                return key==null?"minecraft:air":key.toString();
            });
            reply(ex,200,"{\"ok\":true,\"block\":\""+jsonEscape(result)+"\"}");
        } catch(Exception e) {
            reply(ex,400,errorJson(e));
        }
    }

    private static BlockState resolveBlock(String id) {
        for (Block block : BuiltInRegistries.BLOCK) {
            var key = BuiltInRegistries.BLOCK.getKey(block);
            if (key != null && key.toString().equals(id)) return block.defaultBlockState();
        }
        throw new IllegalArgumentException("unknown block: " + id);
    }

    private static ServerLevel level() {
        MinecraftServer s=server;
        if(s==null) throw new IllegalStateException("server is not ready");
        return s.overworld();
    }

    private static <T> T onServer(java.util.concurrent.Callable<T> call) throws Exception {
        MinecraftServer s=server;
        if(s==null) throw new IllegalStateException("server is not ready");
        CompletableFuture<T> f=new CompletableFuture<>();
        s.execute(() -> {
            try { f.complete(call.call()); }
            catch(Throwable t) { f.completeExceptionally(t); }
        });
        return f.get(30,TimeUnit.SECONDS);
    }

    private static String body(HttpExchange ex) throws IOException {
        return new String(ex.getRequestBody().readAllBytes(),StandardCharsets.UTF_8);
    }

    private static void reply(HttpExchange ex,int status,String payload) throws IOException {
        byte[] bytes=payload.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type","application/json; charset=utf-8");
        ex.sendResponseHeaders(status,bytes.length);
        try(var os=ex.getResponseBody()) { os.write(bytes); }
    }

    private static String errorJson(Exception e) {
        return "{\"ok\":false,\"error\":\""+jsonEscape(String.valueOf(e.getMessage()))+"\"}";
    }

    private static String jsonEscape(String value) {
        if(value==null) return "";
        return value.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n").replace("\r","\\r");
    }
}
