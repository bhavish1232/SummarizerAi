import { useState } from 'react';

export default function PromptBox({ onGenerate }) {
  const [prompt, setPrompt] = useState('Summarize in bullet points for executives with <h2> headings and <ul><li> lists, ending with an <h2>Action Items</h2> section.');
  return (
    <div style={{display:'grid', gap:8}}>
      <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} style={{width:'100%'}} />
      <button onClick={()=>onGenerate(prompt)}>Generate Summary</button>
    </div>
  );
}
