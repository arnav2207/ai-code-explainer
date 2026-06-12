interface Props {
  explanation: string | null;
}

export function ExplanationPanel({
  explanation,
}: Props) {
  if (!explanation) {
    return (
      <div className="rounded-lg border p-6">
        No explanation generated yet.
      </div>
    );
  }

  return (
    <div className="rounded-lg border p-6">
      {explanation}
    </div>
  );
}