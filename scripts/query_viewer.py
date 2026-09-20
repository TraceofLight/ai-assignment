"""과제 SQL을 새 메모리 DB에서 실행하고 캡처 가능한 클라이언트 화면에 표시한다."""

import sqlite3
import tkinter as tk
from tkinter import ttk

import run


JOIN_COMPARISON = """-- Q15 실행 후: 주문 없는 한예린 고객의 포함 여부를 비교한다.
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count
FROM customer AS c
LEFT JOIN cafe_order AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count
FROM customer AS c
INNER JOIN cafe_order AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
"""


def execute_block(connection, block):
    """화면에 표시할 SQL을 실행하고 기존 파이프라인과 같은 형식으로 결과를 반환한다."""
    output = []
    for statement in run._split_statements(block):
        body = run._statement_body(statement)
        if not body:
            continue
        cursor = connection.execute(body)
        keyword = body.split(None, 1)[0].upper()
        if cursor.description is not None:
            output.append(run._format_rows(cursor))
        elif keyword in {"UPDATE", "DELETE"}:
            output.append(f"{keyword} 적용 행 수: {cursor.rowcount}")
        else:
            output.append(f"{keyword} 실행 완료")
    connection.commit()
    return "\n\n".join(output)


def main():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(run._read_sql(run.SQL_DIR / "schema.sql"))
    connection.executescript(run._read_sql(run.SQL_DIR / "seed.sql"))
    blocks = run._query_blocks(run._read_sql(run.SQL_DIR / "queries.sql"))
    blocks.append(JOIN_COMPARISON)
    window = tk.Tk()
    window.title("카페 주문 SQL 실행 클라이언트 | Python sqlite3")
    window.geometry("1440x1000")
    heading = ttk.Label(window, font=("맑은 고딕", 14, "bold"))
    heading.pack(padx=16, pady=8, anchor="w")
    ttk.Label(window, text=f"SQLite {sqlite3.sqlite_version} | 새 메모리 DB | FK ON | Q01 → Q15 순차 실행 | 마지막 화면: Q15 이후 JOIN 비교").pack(padx=16, anchor="w")
    panes = ttk.Panedwindow(window, orient=tk.HORIZONTAL)
    panes.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
    sql_text = tk.Text(panes, wrap="word", font=("맑은 고딕", 11), padx=12, pady=12)
    result_text = tk.Text(panes, wrap="none", font=("맑은 고딕", 11), padx=12, pady=12)
    panes.add(sql_text, weight=1)
    panes.add(result_text, weight=1)
    position = 0

    def advance():
        nonlocal position
        block = blocks[position]
        result = execute_block(connection, block)
        label = f"Q{position + 1:02d}" if position < 15 else "JOIN-comparison (Q15 실행 후)"
        heading.configure(text=f"{label} — 실행한 SQL / 실제 실행 결과")
        for widget, value in [(sql_text, block), (result_text, result)]:
            widget.configure(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", value)
            widget.configure(state="disabled")
        position += 1
        if position == len(blocks):
            button.configure(state="disabled")

    button = ttk.Button(window, text="다음 쿼리 실행", command=advance)
    button.pack(pady=8)
    advance()
    window.mainloop()
    connection.close()


if __name__ == "__main__":
    main()
