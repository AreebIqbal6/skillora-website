const fs = require('fs');
const readline = require('readline');

async function processLineByLine() {
  const fileStream = fs.createReadStream('C:\\\\Users\\\\Noman Traders\\\\.gemini\\\\antigravity\\\\brain\\\\ddb5f484-14d4-4232-81c4-935d633885ec\\\\.system_generated\\\\logs\\\\transcript_full.jsonl', { encoding: 'utf8' });
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  for await (const line of rl) {
    if (line.includes('.nav-pill') && line.includes('backdrop-filter')) {
        const data = JSON.parse(line);
        if (data.tool_calls) {
           for (let call of data.tool_calls) {
               if (call.name === 'multi_replace_file_content' || call.name === 'write_to_file') {
                   console.log('FOUND CSS MATCH in step:', data.step_index);
                   console.log(JSON.stringify(call.args).substring(0, 5000));
                   console.log('---');
               }
           }
        }
    }
  }
}

processLineByLine();
