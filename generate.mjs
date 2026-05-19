#!/usr/bin/env node
/**
 * Higgsfield Video Generator — 两步流水线
 * Step 1: 文字 → 静帧  (Seedream v4)
 * Step 2: 静帧 → 视频  (Kling 2.1 Pro)
 *
 * 使用: node generate.mjs --prompt "..." [选项]
 * Auth: export HF_CREDENTIALS="KEY_ID:KEY_SECRET"
 */

import { higgsfield, config } from '@higgsfield/client/v2';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';
import https from 'https';
import { parseArgs } from 'util';

// ── Auth ──────────────────────────────────────────────────────────────────────
const creds = process.env.HF_CREDENTIALS;
if (!creds || !creds.includes(':')) {
  console.error('❌ 未找到凭证。请先运行:\n   export HF_CREDENTIALS="KEY_ID:KEY_SECRET"');
  process.exit(1);
}
config({ credentials: creds });

// ── Args ──────────────────────────────────────────────────────────────────────
const { values: args } = parseArgs({
  options: {
    prompt:       { type: 'string' },
    'image-prompt': { type: 'string' },
    aspect:       { type: 'string', default: '9:16' },
    duration:     { type: 'string', default: '5' },
    output:       { type: 'string', default: 'output.mp4' },
    'image-only': { type: 'boolean', default: false },
    'image-url':  { type: 'string' },
  }
});

if (!args.prompt) {
  console.error('❌ --prompt 必填');
  process.exit(1);
}

const ASPECT_MAP = { '9:16': '2:3', '16:9': '3:2', '1:1': '1:1', '4:3': '4:3' };
const imagePrompt = args['image-prompt'] || args.prompt;
const duration    = parseInt(args.duration, 10);
const outputPath  = args.output;

// ── Download helper ───────────────────────────────────────────────────────────
async function download(url, dest) {
  return new Promise((resolve, reject) => {
    const file = createWriteStream(dest);
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        file.close();
        return download(res.headers.location, dest).then(resolve).catch(reject);
      }
      res.pipe(file);
      file.on('finish', () => file.close(resolve));
    }).on('error', reject);
  });
}

// ── Main ──────────────────────────────────────────────────────────────────────
let imageUrl = args['image-url'];

if (!imageUrl) {
  // Step 1: 文字 → 静帧
  console.log(`\n🖼  Step 1/2 — 生成首帧 (bytedance/seedream/v4/text-to-image)`);
  console.log(`  提示词: ${imagePrompt.slice(0, 80)}${imagePrompt.length > 80 ? '...' : ''}`);

  const imgJob = await higgsfield.subscribe('bytedance/seedream/v4/text-to-image', {
    input: {
      prompt: imagePrompt,
      aspect_ratio: ASPECT_MAP[args.aspect] || '2:3',
    },
    withPolling: true,
  });

  if (imgJob.status !== 'completed') {
    console.error(`❌ 图片生成失败: ${imgJob.status}`);
    console.error(JSON.stringify(imgJob, null, 2));
    process.exit(1);
  }

  imageUrl = imgJob.images?.[0]?.url;
  if (!imageUrl) {
    console.error('❌ 响应中未找到 image URL:', JSON.stringify(imgJob, null, 2));
    process.exit(1);
  }
  console.log(`  ✓ 图片 URL: ${imageUrl}`);

  if (args['image-only']) {
    const imgPath = outputPath.endsWith('.mp4') ? outputPath.replace('.mp4', '.jpg') : outputPath + '.jpg';
    process.stdout.write('\n⬇️  下载图片...');
    await download(imageUrl, imgPath);
    console.log(`\n✅ 完成: ${imgPath}`);
    process.exit(0);
  }
} else {
  console.log(`⏭  跳过 Step 1，使用提供的图片 URL`);
}

// Step 2: 静帧 → 视频
console.log(`\n🎬 Step 2/2 — 生成视频 (kling-video/v2.1/pro/image-to-video)`);
console.log(`  比例: ${args.aspect}  时长: ${duration}s`);
process.stdout.write('  生成中，请稍候（约 2-4 分钟）...');

const vidJob = await higgsfield.subscribe('kling-video/v2.1/pro/image-to-video', {
  input: {
    prompt: args.prompt,
    image_url: imageUrl,
    aspect_ratio: args.aspect,
    duration: duration,
  },
  withPolling: true,
});

console.log('');

if (vidJob.status !== 'completed') {
  console.error(`❌ 视频生成失败: ${vidJob.status}`);
  console.error(JSON.stringify(vidJob, null, 2));
  process.exit(1);
}

const videoUrl = vidJob.video?.url;
if (!videoUrl) {
  console.error('❌ 响应中未找到 video URL:', JSON.stringify(vidJob, null, 2));
  process.exit(1);
}

process.stdout.write('\n⬇️  下载视频...');
await download(videoUrl, outputPath);
console.log(`\n✅ 完成！视频保存至: ${outputPath}`);
console.log(`   原始 URL: ${videoUrl}`);
