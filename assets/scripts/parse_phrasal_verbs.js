/*
 Parses phrasal_verbs.txt into a structured JSON file phrasal_verbs.json
 Schema:
 [
   {
     id: number,
     verb: string,
     senses: [
       {
         senseNumber: number,
         definition: string,        // definition text (without trailing percentage)
         confidencePercent: number, // numeric percentage from the line's trailing (...%)
         examples: string[]         // concatenated example lines for this sense
       }
     ]
   }
 ]
*/

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const inputPath = path.resolve(__dirname, '..', 'phrasal_verbs.txt');
const outputPath = path.resolve(__dirname, '..', 'phrasal_verbs.json');

function isHeaderLine(line) {
  const trimmed = line.trim();
  return /^\d+\.\s+[A-Z][A-Z\s\-']+$/.test(trimmed);
}

function isSenseStartLine(line) {
  const trimmed = line.trim();
  return /^\d+\.\s+/.test(trimmed);
}

function isPercentTerminated(line) {
  const trimmed = line.trim();
  return /\(\d+(?:\.\d+)?\s*%?\)\s*$/.test(trimmed);
}

function parseHeader(line) {
  const trimmed = line.trim();
  const match = trimmed.match(/^(\d+)\.\s+([A-Z][A-Z\s\-']+)$/);
  if (!match) return null;
  return {
    id: Number(match[1]),
    verb: match[2].trim(),
  };
}

function parseSense(defLines) {
  const first = defLines[0].trim();
  const combined = defLines.map(l => l.trim()).join(' ');
  const numberMatch = first.match(/^(\d+)\./);
  const senseNumber = numberMatch ? Number(numberMatch[1]) : null;

  const confMatch = combined.match(/\((\d+(?:\.\d+)?)\s*%?\)\s*$/);
  const confidencePercent = confMatch ? Number(confMatch[1]) : null;

  let definition = combined
    .replace(/^\d+\.\s+/, '')
    .replace(/\((\d+(?:\.\d+)?)\s*%?\)\s*$/, '')
    .trim();

  definition = definition.replace(/\s+/g, ' ').trim();

  return { senseNumber, definition, confidencePercent };
}

function main() {
  if (!fs.existsSync(inputPath)) {
    console.error(`Input file not found: ${inputPath}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(inputPath, 'utf8');
  const lines = raw.split(/\r?\n/);

  const entries = [];
  let i = 0;
  let currentEntry = null;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) { i += 1; continue; }

    if (isHeaderLine(trimmed)) {
      // Start a new entry
      const header = parseHeader(trimmed);
      if (header) {
        currentEntry = { id: header.id, verb: header.verb, senses: [] };
        entries.push(currentEntry);
        i += 1;
        continue;
      }
    }

    if (isSenseStartLine(trimmed)) {
      if (!currentEntry) {
        // In case file starts unexpectedly, create a placeholder entry
        currentEntry = { id: null, verb: 'UNKNOWN', senses: [] };
        entries.push(currentEntry);
      }

      // Gather potential multiline sense definition until we hit a line ending with percent
      const defLines = [trimmed];
      i += 1;
      while (i < lines.length && !isPercentTerminated(defLines[defLines.length - 1])) {
        const cont = lines[i].trim();
        if (!cont) { i += 1; continue; }
        defLines.push(cont);
        i += 1;
      }

      // If we exited because i == lines.length and last line not percent-terminated,
      // we still attempt to parse whatever was gathered.
      const senseMeta = parseSense(defLines);

      // Now collect example block until next header or next sense start
      const examples = [];
      while (i < lines.length) {
        const nextLine = lines[i];
        const nextTrimmed = nextLine.trim();
        if (!nextTrimmed) { i += 1; continue; }
        if (isHeaderLine(nextTrimmed) || isSenseStartLine(nextTrimmed)) {
          break;
        }
        examples.push(nextTrimmed);
        i += 1;
      }

      const exampleJoined = examples.join(' ').replace(/\s+/g, ' ').trim();
      currentEntry.senses.push({
        senseNumber: senseMeta.senseNumber,
        definition: senseMeta.definition,
        confidencePercent: senseMeta.confidencePercent,
        examples: exampleJoined ? [exampleJoined] : [],
      });

      // Do not i++ here; loop continues from current i to evaluate next header/sense
      continue;
    }

    // If the line is neither a header nor a sense (e.g., stray text), advance
    i += 1;
  }

  // Sort entries by id to be safe
  entries.sort((a, b) => (a.id ?? 0) - (b.id ?? 0));

  fs.writeFileSync(outputPath, JSON.stringify(entries, null, 2), 'utf8');
  console.log(`Wrote ${entries.length} entries to ${outputPath}`);
}

main();


