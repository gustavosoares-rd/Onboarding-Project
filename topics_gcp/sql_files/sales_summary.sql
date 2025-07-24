SELECT region, SUM(sales) AS total_sales
      FROM raw.sales
      GROUP BY region