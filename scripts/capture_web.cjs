#!/usr/bin/env node
/*
 * Screenshots and demo videos of a web page, driven by the installed Google Chrome.
 * Run scripts/setup_capture.sh once first.
 *
 * Single screenshot:
 *   node capture_web.cjs shot --url http://localhost:5173 --out docs/assets/home.png \
 *        [--width 1280] [--height 800] [--scale 2] [--full-page] [--dark] [--wait 800] [--selector ".card"]
 *
 * Scripted scenario (screenshots and/or one video of the whole run):
 *   node capture_web.cjs scenario docs/demo/scenario.json
 *
 * Scenario file:
 * {
 *   "baseUrl": "http://localhost:5173",
 *   "viewport": {"width": 1280, "height": 800},
 *   "scale": 2,                       // device pixel ratio for screenshots (video ignores it)
 *   "colorScheme": "light",           // or "dark"
 *   "cursor": true,                   // draw a visible cursor (useful in videos)
 *   "video": "docs/demo/demo.webm",   // optional, convert with make_gif.sh afterwards
 *   "steps": [
 *     {"goto": "/"},
 *     {"wait": 800},
 *     {"screenshot": "docs/assets/home.png"},
 *     {"click": "text=New project"},
 *     {"type": {"selector": "#name", "text": "My report", "delay": 70}},
 *     {"press": "Enter"},
 *     {"waitFor": ".result"},
 *     {"hover": ".card >> nth=0"},
 *     {"scroll": 600},
 *     {"screenshot": {"path": "docs/assets/result.png", "selector": ".panel", "fullPage": false}}
 *   ]
 * }
 * Paths in the scenario are resolved from the current working directory.
 */
const fs = require("fs");
const os = require("os");
const path = require("path");

const CACHE = process.env.READMEFORGE_CACHE || path.join(os.homedir(), ".cache", "readme-forge");
let chromium;
try {
  ({ chromium } = require(path.join(CACHE, "node_modules", "playwright-core")));
} catch {
  console.error(`playwright-core not found in ${CACHE}. Run scripts/setup_capture.sh first.`);
  process.exit(1);
}

const CURSOR_SCRIPT = `
  window.addEventListener('DOMContentLoaded', () => {
    const c = document.createElement('div');
    c.id = '__rf_cursor';
    Object.assign(c.style, {position:'fixed', zIndex: 2147483647, width:'18px', height:'18px',
      marginLeft:'-9px', marginTop:'-9px', borderRadius:'50%', pointerEvents:'none',
      background:'rgba(20,20,20,0.35)', border:'2px solid rgba(255,255,255,0.9)',
      boxShadow:'0 1px 4px rgba(0,0,0,0.35)', transition:'transform 120ms ease', left:'-50px', top:'-50px'});
    document.body.appendChild(c);
    document.addEventListener('mousemove', e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; }, true);
    document.addEventListener('mousedown', () => { c.style.transform = 'scale(0.7)'; }, true);
    document.addEventListener('mouseup', () => { c.style.transform = 'scale(1)'; }, true);
  });`;

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) out[key] = true;
      else { out[key] = next; i++; }
    } else out._.push(a);
  }
  return out;
}

async function launch() {
  const opts = { headless: true };
  if (process.env.CHROME_PATH) opts.executablePath = process.env.CHROME_PATH;
  else opts.channel = "chrome";
  try {
    return await chromium.launch(opts);
  } catch (e) {
    console.error("Could not start Chrome. Install Google Chrome or set CHROME_PATH.\n" + e.message);
    process.exit(1);
  }
}

function ensureDir(file) {
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
}

async function moveTo(page, selector) {
  const loc = page.locator(selector).first();
  await loc.scrollIntoViewIfNeeded();
  const box = await loc.boundingBox();
  if (box) await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 25 });
  return loc;
}

async function shot(args) {
  if (!args.url || !args.out) {
    console.error("shot needs --url and --out");
    process.exit(2);
  }
  const browser = await launch();
  const context = await browser.newContext({
    viewport: { width: Number(args.width || 1280), height: Number(args.height || 800) },
    deviceScaleFactor: Number(args.scale || 2),
    colorScheme: args.dark ? "dark" : "light",
  });
  const page = await context.newPage();
  await page.goto(args.url, { waitUntil: "networkidle" });
  await page.waitForTimeout(Number(args.wait || 500));
  ensureDir(args.out);
  if (args.selector) await page.locator(args.selector).first().screenshot({ path: args.out });
  else await page.screenshot({ path: args.out, fullPage: Boolean(args["full-page"]) });
  await browser.close();
  console.log(`saved ${args.out}`);
}

async function scenario(file) {
  const sc = JSON.parse(fs.readFileSync(file, "utf8"));
  const viewport = sc.viewport || { width: 1280, height: 800 };
  const browser = await launch();
  const ctxOpts = { viewport, deviceScaleFactor: sc.scale || 2, colorScheme: sc.colorScheme || "light" };
  let videoDir;
  if (sc.video) {
    videoDir = fs.mkdtempSync(path.join(os.tmpdir(), "rf-video-"));
    ctxOpts.recordVideo = { dir: videoDir, size: viewport };
  }
  const context = await browser.newContext(ctxOpts);
  if (sc.cursor) await context.addInitScript(CURSOR_SCRIPT);
  const page = await context.newPage();
  const url = (u) => (/^[a-z]+:/i.test(u) ? u : (sc.baseUrl || "").replace(/\/$/, "") + u);

  let failure = null;
  try {
  for (const step of sc.steps || []) {
    const [kind, val] = Object.entries(step)[0];
    switch (kind) {
      case "goto": await page.goto(url(val), { waitUntil: "networkidle" }); break;
      case "wait": await page.waitForTimeout(Number(val)); break;
      case "waitFor": await page.locator(val).first().waitFor({ timeout: 15000 }); break;
      case "click": {
        const loc = await moveTo(page, val);
        await page.waitForTimeout(150);
        await loc.click();
        break;
      }
      case "hover": await moveTo(page, val); break;
      case "type": {
        const loc = await moveTo(page, val.selector);
        await loc.click();
        await page.keyboard.type(val.text, { delay: val.delay ?? 60 });
        break;
      }
      case "fill": await page.locator(val.selector).first().fill(val.text); break;
      case "press": await page.keyboard.press(val); break;
      case "select": await page.locator(val.selector).first().selectOption(val.value); break;
      case "scroll": await page.mouse.wheel(0, Number(val)); await page.waitForTimeout(400); break;
      case "eval": await page.evaluate(val); break;
      case "screenshot": {
        const o = typeof val === "string" ? { path: val } : val;
        ensureDir(o.path);
        if (o.selector) await page.locator(o.selector).first().screenshot({ path: o.path });
        else await page.screenshot({ path: o.path, fullPage: Boolean(o.fullPage) });
        console.log(`saved ${o.path}`);
        break;
      }
      default: console.error(`unknown step: ${kind}`); process.exitCode = 2;
    }
  }
  } catch (e) {
    failure = e;
  }
  const video = sc.video ? page.video() : null;
  await context.close();
  if (video) {
    ensureDir(sc.video);
    await video.saveAs(sc.video);
    fs.rmSync(videoDir, { recursive: true, force: true });
    console.log(`saved ${sc.video} (convert with make_gif.sh)`);
  }
  await browser.close();
  if (failure) throw failure;
}

(async () => {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  if (cmd === "shot") await shot(args);
  else if (cmd === "scenario" && args._[1]) await scenario(args._[1]);
  else {
    console.error("usage: capture_web.cjs shot --url URL --out FILE [...] | scenario FILE.json");
    process.exit(2);
  }
})().catch((e) => { console.error(e); process.exit(1); });
