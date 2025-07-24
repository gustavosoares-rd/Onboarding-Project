SELECT region, total_sales
      FROM {{ ref('sales_summary') }}
      WHERE total_sales > 1000