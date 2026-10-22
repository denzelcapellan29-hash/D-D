"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const src=fs.readFileSync(path.join(__dirname, "../module/acq-foundry-bridge/scripts/acq-foundry-bridge.js"), "utf8");
const start=src.indexOf("async function request(path, options = {}) {");
const end=src.indexOf("async function postState(",start);
assert.ok(start>=0 && end>start,"expected first-party loopback fetch helper");
const helper=src.slice(start,end);

test("GM bridge aborts a hung GET rather than holding the poll forever",async()=>{
  let aborts=0;
  const ctx={
    agentUrl:()=> "http://127.0.0.1:18747",
    fetch:(_url,opts)=>new Promise((_res,rej)=>{
      opts.signal.addEventListener("abort",()=>{aborts++;rej(new Error("aborted"));},{once:true});
    }),
    AbortController,setTimeout,clearTimeout
  };
  vm.runInNewContext(helper+"; globalThis.loopRequest=request;",ctx);
  await assert.rejects(()=>ctx.loopRequest("/bridge/next",{method:"GET",timeoutMs:1000}),/aborted/);
  assert.equal(aborts,1);
});

test("GM bridge forwards 204 and clears request timeout normally",async()=>{
  const ctx={
    agentUrl:()=> "http://127.0.0.1:18747",
    fetch:async(_url,opts)=>({status:204, signalAborted:opts.signal.aborted}),
    AbortController,setTimeout,clearTimeout
  };
  vm.runInNewContext(helper+"; globalThis.loopRequest=request;",ctx);
  const response=await ctx.loopRequest("/bridge/next",{method:"GET",timeoutMs:1000});
  assert.equal(response.status,204);
  assert.equal(response.signalAborted,false);
});
