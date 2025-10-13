WITH
  TotalCustomers AS (
    SELECT COUNT(DISTINCT customer_id) AS total_clientes
    FROM `seu-projeto-id-aqui.loja_virtual_tratado.customers`
  ),
  PurchasingCustomers AS (
    SELECT COUNT(DISTINCT customer_id) AS clientes_compradores
    FROM `seu-projeto-id-aqui.loja_virtual_tratado.orders`
  )
SELECT
  tc.total_clientes,
  pc.clientes_compradores,
  (pc.clientes_compradores / tc.total_clientes) AS taxa_de_conversao
FROM TotalCustomers AS tc, PurchasingCustomers AS pc;
