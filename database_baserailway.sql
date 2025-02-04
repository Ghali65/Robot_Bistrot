-- Création de la base de données
CREATE DATABASE search_and_go;

-- Connexion à la base de données
\c search_and_go;

-- Création de la table user
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,  -- Identifiant utilisateur, clé primaire avec auto-incrémentation
    first_name VARCHAR(50) NOT NULL,  -- Prénom de l'utilisateur
    last_name VARCHAR(50) NOT NULL,  -- Nom de l'utilisateur
    email VARCHAR(100) UNIQUE NOT NULL,  -- Adresse email unique
    password VARCHAR(255) NOT NULL  -- Mot de passe (stocké de manière sécurisée)
);

-- Création de la table restaurants
CREATE TABLE restaurants (
    restaurant_id VARCHAR(255) PRIMARY KEY,  -- Identifiant restaurant, clé primaire
    name VARCHAR(255) NOT NULL,  -- Nom du restaurant
    lat NUMERIC(10, 7) NOT NULL,  -- Latitude du restaurant
    lng NUMERIC(10, 7) NOT NULL,  -- Longitude du restaurant
    formatted_address VARCHAR(255) NOT NULL,  -- Adresse formatée
    photo_reference TEXT,  -- Référence de la photo (facultatif)
    rating NUMERIC(3, 2),  -- Note moyenne (facultatif)
    user_ratings_total INTEGER,  -- Nombre total d'avis utilisateurs (facultatif)
    types TEXT[]  -- Types de restaurants sous forme de tableau
);

-- Création de la table query
CREATE TABLE query (
    query_id SERIAL PRIMARY KEY,  -- Identifiant de la requête, clé primaire avec auto-incrémentation
    user_id INTEGER NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,  -- Clé étrangère vers la table user
    name VARCHAR(255) NOT NULL,  -- Nom de la requête (par exemple, description de l'action)
    lat NUMERIC(10, 7) NOT NULL,  -- Latitude du lieu recherché
    lng NUMERIC(10, 7) NOT NULL,  -- Longitude du lieu recherché
    formatted_address VARCHAR(255) NOT NULL,  -- Adresse formatée du lieu recherché
    photo_reference TEXT,  -- Référence de la photo (facultatif)
    rating NUMERIC(3, 2),  -- Note moyenne (facultatif)
    user_ratings_total INTEGER,  -- Nombre total d'avis utilisateurs (facultatif)
    types TEXT[]  -- Types d'endroits recherchés sous forme de tableau
);
