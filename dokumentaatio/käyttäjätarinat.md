# Käyttäjätarinat

* Käyttäjänä voin selata listaa kehitysehdotuksista
```SQL
SELECT Feature.*,
        (SELECT COUNT(*)
            FROM "like"
            WHERE feature_id=Feature.id) AS like_count,
        (SELECT COUNT(*)
            FROM "like"
            WHERE feature_id=Feature.id AND user_id=%(current_user)s ) AS current_user_liked
FROM Feature
WHERE category_id=%(category_id)s
ORDER BY like_count DESC
LIMIT %(page_size)s
OFFSET %(skip_count)s
```
* Käyttäjänä voin rekisteröityä
```SQL
INSERT INTO account (date_created, date_modified, username, password, is_admin) 
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(username)s, %(password)s, %(is_admin)s) 
RETURNING account.id
```
* Käyttäjänä voin kirjautua käyttäjänimellä ja salasanalla
```SQL
SELECT account.id AS account_id, account.date_created AS account_date_created, account.date_modified AS account_date_modified, account.username AS account_username, account.password AS account_password, account.is_admin AS account_is_admin
FROM account
WHERE account.username = %(username_1)s
LIMIT %(param_1)s
```
* Rekisteröityneenä käyttäjänä voin lisätä uuden kehitysehdotuksen
```SQL
INSERT INTO feature (date_created, date_modified, user_id, title, description, category_id)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s, %(title)s, %(description)s, %(category_id)s)
RETURNING feature.id
```
* Rekisteröityneenä käyttäjänä voin muokata omaa kehitysehdotusta
```SQL
UPDATE feature 
SET date_modified=CURRENT_TIMESTAMP, 
    title=%(title)s, 
    description=%(description)s
WHERE feature.id = %(feature_id)s
```
* Rekisteröityneenä käyttäjänä voin äänestää toisten kehitysehdotuksia
```SQL
INSERT INTO "like" (date_created, date_modified, user_id, feature_id)
VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %(user_id)s, %(feature_id)s) 
RETURNING "like".id
```
* Rekisteröityneenä käyttäjänä voin poistaa ääneni ehdotukselta
```
DELETE FROM "like" WHERE "like".id = %(id)s
```
* Ylläpitäjänä voin poistaa ehdotuksen
```
DELETE FROM feature WHERE feature.id = %(id)s
```
* Ylläpitäjänä voin vaihtaa ehdotuksen kategoriaa
```
UPDATE feature 
SET date_modified=CURRENT_TIMESTAMP, category_id=%(category_id)s 
WHERE feature.id = %(feature_id)s
```
