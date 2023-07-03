CREATE SCHEMA amigo;

CREATE TABLE user_info(
   uid INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   email varchar(255) NOT NULL,
   first_name varchar(255),
   middle_name varchar(255),
   last_name varchar(255), 
   country_code varchar(5),
   phone_number bigint,
   preferred_country varchar(255),
   profile_completion_status varchar(255) NOT NULL,
   ts_added timestamp NOT NULL,
   ts_updated timestamp,
   ts_Deactivated timestamp,
   is_active boolean NOT NULL,
);

CREATE TABLE user_scores(
   uid INT PRIMARY KEY,
   gre smallint,
   ielts smallint,
   tofel smallint,
   gmat smallint,
   CONSTRAINT fk_user_info
      FOREIGN KEY(uid) 
	      REFERENCES user_info(uid)
         ON DELETE CASCADE                
);

CREATE TABLE user_login(
   uid INT PRIMARY KEY,
   email varchar(255) NOT NULL,
   hashed_password varchar NOT NULL,
   ts_added timestamp NOT NULL, 
   CONSTRAINT fk_user_info
      FOREIGN KEY(uid) 
	      REFERENCES user_info(uid)
         ON DELETE CASCADE                
)

CREATE TABLE user_files(
   uid INT,
   file_type varchar(20) NOT NULL,
   s3_urls varchar NOT NULL, 
   PRIMARY KEY(uid, file_type)
   CONSTRAINT fk_user_info
      FOREIGN KEY(uid) 
	      REFERENCES user_info(uid)
         ON DELETE CASCADE                
);

