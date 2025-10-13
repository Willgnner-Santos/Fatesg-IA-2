SELECT
    oi.order_item_id, oi.quantity, oi.unit_price, o.order_id, o.order_date,
    o.total_amount, o.payment_method, p.product_id, p.product_name,
    p.category, p.price AS product_current_price, p.brand, c.customer_id,
    c.name AS customer_name, c.gender, c.signup_date, c.country, pr.review_id,
    pr.rating, pr.review_date
FROM
    `seu-projeto-id-aqui.loja_virtual_tratado.order_items` AS oi
LEFT JOIN `seu-projeto-id-aqui.loja_virtual_tratado.orders` AS o ON oi.order_id = o.order_id
LEFT JOIN `seu-projeto-id-aqui.loja_virtual_tratado.products` AS p ON oi.product_id = p.product_id
LEFT JOIN `seu-projeto-id-aqui.loja_virtual_tratado.customers` AS c ON o.customer_id = c.customer_id
LEFT JOIN `seu-projeto-id-aqui.loja_virtual_tratado.product_reviews` AS pr ON p.product_id = pr.product_id AND c.customer_id = pr.customer_id;
