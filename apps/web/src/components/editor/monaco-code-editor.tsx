"use client";

import Editor from "@monaco-editor/react";

interface MonacoCodeEditorProps {
  language: string;
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
}

export function MonacoCodeEditor({
  language,
  value,
  onChange,
  height = "500px",
  readOnly = false,
}: MonacoCodeEditorProps) {
  return (
    <div className="overflow-hidden rounded-lg border shadow-sm">
      <Editor
        height={height}
        language={language}
        theme="vs-dark"
        value={value}
        onChange={(value) => onChange(value ?? "")}
        options={{
          readOnly,
          minimap: {
            enabled: false,
          },
          fontSize: 14,
          wordWrap: "on",
          automaticLayout: true,
          scrollBeyondLastLine: false,
          tabSize: 2,
          padding: {
            top: 16,
            bottom: 16,
          },
          smoothScrolling: true,
          cursorBlinking: "smooth",
          roundedSelection: true,
          formatOnPaste: true,
          formatOnType: true,
        }}
      />
    </div>
  );
}

export default MonacoCodeEditor;