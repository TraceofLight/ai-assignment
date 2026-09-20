-- 테이블/PK 역할: customer.customer_id 고객 식별, staff.staff_id 직원 식별,
-- menu_category.category_id 분류 식별, menu_item.menu_item_id 메뉴 식별,
-- cafe_order.order_id 주문 식별, order_item.order_item_id 주문 상세 행 식별.
-- 부모 1 : 자식 N 관계 (부모는 자식 0개도 허용):
-- menu_category -> menu_item(category_id), customer -> cafe_order(customer_id),
-- staff -> cafe_order(staff_id), cafe_order -> order_item(order_id),
-- menu_item -> order_item(menu_item_id). 모든 FK는 NOT NULL로 부모 하나를 참조한다.
-- DATE/DATETIME은 SQLite에서 날짜 유효성을 강제하지 않는다. 시드는 ISO 형식 TEXT를 사용한다.
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS cafe_order;
DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS menu_category;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS customer;

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    joined_at DATE NOT NULL,
    city TEXT NOT NULL,
    membership_level TEXT NOT NULL CHECK (membership_level IN ('regular', 'silver', 'gold'))
);

CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    hired_at DATE NOT NULL
);

CREATE TABLE menu_category (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    display_order INTEGER NOT NULL CHECK (display_order > 0)
);

CREATE TABLE menu_item (
    menu_item_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    price INTEGER NOT NULL CHECK (price > 0),
    is_available INTEGER NOT NULL DEFAULT 1 CHECK (is_available IN (0, 1)),
    created_at DATE NOT NULL,
    FOREIGN KEY (category_id) REFERENCES menu_category(category_id)
);

CREATE TABLE cafe_order (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    staff_id INTEGER NOT NULL,
    ordered_at DATETIME NOT NULL,
    order_type TEXT NOT NULL CHECK (order_type IN ('takeout', 'dine_in', 'delivery')),
    status TEXT NOT NULL CHECK (status IN ('pending', 'paid', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
);

CREATE TABLE order_item (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price INTEGER NOT NULL CHECK (unit_price > 0),
    FOREIGN KEY (order_id) REFERENCES cafe_order(order_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(menu_item_id)
);
