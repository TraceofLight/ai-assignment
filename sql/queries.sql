-- Q01. 서울 강남구 고객만 조회해 지역 조건 검색을 확인한다.
-- 의도: 강남구 고객을 선별한다.
SELECT customer_id, name, city, membership_level
FROM customer
WHERE city = '서울 강남구'
ORDER BY customer_id;

-- Q02. 판매 가능한 메뉴를 가격이 높은 순서로 정렬한다.
-- 의도: 판매 가능한 메뉴의 가격 순위를 확인한다.
SELECT menu_item_id, name, price
FROM menu_item
WHERE is_available = 1
ORDER BY price DESC, name ASC;

-- Q03. 최근 주문 5건만 조회해 LIMIT 사용을 확인한다.
-- 의도: 최신 주문 다섯 건을 확인한다.
SELECT order_id, customer_id, ordered_at, order_type, status
FROM cafe_order
ORDER BY ordered_at DESC
LIMIT 5;

-- Q04. 결제 완료된 포장 주문 중 최근 3건을 조회한다.
-- 의도: 결제 완료 포장 주문만 최근순으로 확인한다.
SELECT order_id, customer_id, ordered_at, status
FROM cafe_order
WHERE order_type = 'takeout' AND status = 'paid'
ORDER BY ordered_at DESC
LIMIT 3;

-- Q05. 주문과 고객, 담당 직원을 INNER JOIN으로 연결해 주문 처리 내역을 조회한다.
-- 의도: 주문별 고객과 담당 직원을 식별한다.
SELECT o.order_id, c.name AS customer_name, s.name AS staff_name, o.ordered_at, o.status
FROM cafe_order AS o
INNER JOIN customer AS c ON o.customer_id = c.customer_id
INNER JOIN staff AS s ON o.staff_id = s.staff_id
ORDER BY o.order_id;

-- Q06. 주문 상세와 메뉴, 카테고리를 INNER JOIN으로 연결해 주문 품목을 조회한다.
-- 의도: 주문 품목의 메뉴명과 분류를 확인한다.
SELECT oi.order_id, mc.name AS category_name, mi.name AS menu_name, oi.quantity, oi.unit_price
FROM order_item AS oi
INNER JOIN menu_item AS mi ON oi.menu_item_id = mi.menu_item_id
INNER JOIN menu_category AS mc ON mi.category_id = mc.category_id
ORDER BY oi.order_id, oi.order_item_id;

-- Q07. 주문별 결제 금액을 JOIN과 GROUP BY로 계산한다.
-- 의도: 결제 완료 주문별 총액을 계산한다.
SELECT o.order_id, c.name AS customer_name, SUM(oi.quantity * oi.unit_price) AS order_total
FROM cafe_order AS o
INNER JOIN customer AS c ON o.customer_id = c.customer_id
INNER JOIN order_item AS oi ON o.order_id = oi.order_id
WHERE o.status = 'paid'
GROUP BY o.order_id, c.name
ORDER BY order_total DESC;

-- Q08. 고객별 주문 수를 LEFT JOIN으로 조회해 주문이 없는 고객도 포함한다.
-- 의도: 주문 유무와 관계없이 고객별 주문 수를 센다.
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count
FROM customer AS c
LEFT JOIN cafe_order AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY order_count ASC, c.customer_id ASC;

-- Q09. 주문 상태별 건수를 COUNT와 GROUP BY로 집계한다.
-- 의도: 상태별 주문 건수를 비교한다.
SELECT status, COUNT(*) AS order_count
FROM cafe_order
GROUP BY status
ORDER BY order_count DESC, status ASC;

-- Q10. 고객별 결제 완료 매출을 SUM과 GROUP BY로 집계한다.
-- 의도: 결제 완료 매출이 있는 고객의 매출 합계를 비교한다.
SELECT c.customer_id, c.name, SUM(oi.quantity * oi.unit_price) AS paid_total
FROM customer AS c
INNER JOIN cafe_order AS o ON c.customer_id = o.customer_id
INNER JOIN order_item AS oi ON o.order_id = oi.order_id
WHERE o.status = 'paid'
GROUP BY c.customer_id, c.name
ORDER BY paid_total DESC;

-- Q11. 주문 방식별 평균 주문 금액을 AVG와 GROUP BY로 집계한다.
-- 의도: 품목 수가 아닌 주문을 기준으로 객단가를 계산한다.
SELECT order_type, ROUND(AVG(order_total), 1) AS average_order_total
FROM (
    SELECT o.order_id, o.order_type, SUM(oi.quantity * oi.unit_price) AS order_total
    FROM cafe_order AS o
    INNER JOIN order_item AS oi ON o.order_id = oi.order_id
    WHERE o.status = 'paid'
    GROUP BY o.order_id, o.order_type
) AS paid_orders
GROUP BY order_type
ORDER BY average_order_total DESC;

-- Q12. 상관 서브쿼리로 전체 고객의 결제 완료 매출을 계산하고 매출이 없으면 0을 표시한다.
-- 의도: 매출 없는 고객까지 0원으로 포함한다.
SELECT c.customer_id,
       c.name,
       (
           SELECT COALESCE(SUM(oi.quantity * oi.unit_price), 0)
           FROM cafe_order AS o
           INNER JOIN order_item AS oi ON o.order_id = oi.order_id
           WHERE o.customer_id = c.customer_id AND o.status = 'paid'
       ) AS paid_total
FROM customer AS c
ORDER BY paid_total DESC, c.customer_id ASC;

-- Q13. 주문 일시 검색을 빠르게 하기 위해 인덱스를 만들고 SQLite 실행 계획을 확인한다.
-- 의도: 기간 검색에서 인덱스 사용 여부를 실행 계획으로 확인한다.
-- 인덱스 이유: 기간별 주문 검색과 최신 주문 정렬은 자주 쓰는 조건이므로 ordered_at에 인덱스를 둔다.
-- 기대 효과: 전체 스캔 대신 범위 탐색으로 검색 비용을 줄일 수 있다. 대상 비율이 높으면 이점이 작고, 작은 시드의 계획만으로 속도 향상을 단정하지 않는다.
-- EXPLAIN QUERY PLAN은 SQLite 전용 실행 계획 확인 문법이다.
CREATE INDEX IF NOT EXISTS idx_cafe_order_ordered_at ON cafe_order(ordered_at);
EXPLAIN QUERY PLAN
SELECT order_id, ordered_at, status
FROM cafe_order
WHERE ordered_at >= '2026-05-04 00:00:00'
ORDER BY ordered_at;

-- Q14. 대기 상태 주문을 결제 완료로 UPDATE하고 변경 결과를 확인한다.
-- 의도: 주문 110의 상태 변경을 검증한다.
UPDATE cafe_order
SET status = 'paid'
WHERE order_id = 110 AND status = 'pending';

SELECT order_id, customer_id, status
FROM cafe_order
WHERE order_id = 110;

-- Q15. 취소 주문을 DELETE하고 주문과 주문 상세가 함께 정리되는지 확인한다.
-- 의도: 주문 112 삭제와 상세의 연쇄 삭제를 확인한다.
DELETE FROM cafe_order
WHERE order_id = 112 AND status = 'cancelled';

SELECT
    (SELECT COUNT(*) FROM cafe_order WHERE order_id = 112) AS remaining_orders,
    (SELECT COUNT(*) FROM order_item WHERE order_id = 112) AS remaining_order_items;
