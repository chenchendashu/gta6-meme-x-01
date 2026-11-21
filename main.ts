// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is a post on X: a GTA 6 meme whose picture is the make.fun
// ghost covering the poster's shift on GTA 6 launch day. This program
// does the one thing the house asks of it: copy POST.json, which names
// the post, from the repository directory to the output directory,
// where the gate reads it.
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Sanity check: POST.json must be a JSON object whose "url" names an X
// (or Twitter) post address -- /<handle>/status/<id>. The placeholder
// the repo ships with passes this shape check; the house still reads
// the real post from X itself.
const POST_URL = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/?#]+\/status\/[^/?#]+$/;

let post: { url?: unknown };
try {
  post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post.url !== 'string' || !POST_URL.test(post.url)) {
  console.error(`POST.json does not name an X post: ${JSON.stringify(post)}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
console.log(`copied POST.json (${post.url}) to ${OUTPUT_DIR}`);
