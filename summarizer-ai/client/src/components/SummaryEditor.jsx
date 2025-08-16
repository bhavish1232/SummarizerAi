import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

export default function SummaryEditor({ html, setHtml }) {
  return (
    <div style={{marginTop:12}}>
      <ReactQuill value={html} onChange={setHtml} />
    </div>
  );
}
