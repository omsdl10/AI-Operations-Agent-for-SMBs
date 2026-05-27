type PaginationControlsProps = {
  page: number;
  pages: number;
  total: number;
  onPageChange: (page: number) => void;
};

export function PaginationControls({ page, pages, total, onPageChange }: PaginationControlsProps) {
  return (
    <div className="flex flex-col gap-3 border-t border-slate-200 bg-white px-4 py-3 text-sm sm:flex-row sm:items-center sm:justify-between">
      <span className="text-slate-600">
        Page {page} of {pages} · {total} total
      </span>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          className="rounded-md border border-slate-200 px-3 py-2 font-medium text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Previous
        </button>
        <button
          type="button"
          onClick={() => onPageChange(page + 1)}
          disabled={page >= pages}
          className="rounded-md border border-slate-200 px-3 py-2 font-medium text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}

