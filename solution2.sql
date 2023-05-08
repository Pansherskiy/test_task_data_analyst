-- Queries executed in PostgreSQL


-- subtask 1
SELECT SUM(loan_amount) / COUNT(*) AS mean_value FROM CreditContracts WHERE DATE_PART('day',NOW() - timestamp) < 60;

SELECT SUM(loan_amount) / COUNT(*) AS median_value FROM
(SELECT *, ROW_NUMBER() OVER (ORDER BY loan_amount DESC) AS desc_loan_amount, ROW_NUMBER() OVER (ORDER BY loan_amount ASC) AS asc_loan_amount
FROM CreditContracts
WHERE DATE_PART('day',NOW() - timestamp) < 60) AS a
WHERE asc_loan_amount IN (desc_loan_amount, desc_loan_amount + 1, desc_loan_amount - 1);

-- To view the result: https://www.db-fiddle.com/f/vP8yP1psQsMd6T91q2BYfV/4


-- subtask 2
SELECT *
FROM CreditApplications
WHERE id NOT IN (
  SELECT MIN(id)
  FROM CreditApplications
  GROUP BY user_id, creditapplication_amount
)
ORDER BY user_id, creditapplication_amount;

-- To view the result: https://www.db-fiddle.com/f/7DbkXvr3vGZukYwdz7jStN/4


-- subtask 3
WITH funnel_events AS (
  SELECT
	county,
	COUNT(CASE WHEN event_type = 'registration' THEN user_id END) AS registrations,
    COUNT(CASE WHEN event_type = 'KYC' THEN user_id END) AS passed_KYC,
    COUNT(CASE WHEN event_type = 'offer' THEN user_id END) AS offers,
    COUNT(CASE WHEN event_type = 'creditcontract' THEN user_id END) AS contracted_loans
  FROM events
  GROUP BY county
)
SELECT
  county,
  registrations,
  passed_KYC,
  offers,
  contracted_loans,
  ROUND(100.0 * contracted_loans / offers, 2) AS contracted_loans_to_offers_rate,
  ROUND(100.0 * contracted_loans / registrations, 2) AS contracted_loans_to_registrations_rate
FROM funnel_events
ORDER BY county;

-- To view the result: https://www.db-fiddle.com/f/3FkK12VmdaoaX2izBKmnRv/2
