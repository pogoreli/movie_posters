-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS project_db;

-- Switch to the project_db database
USE project_db;

DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS vectors;
DROP TABLE IF EXISTS movies;

-- Create the movies table without AUTO_INCREMENT
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT PRIMARY KEY,
    movie_name VARCHAR(255) NOT NULL,
    movie_poster LONGBLOB
);

-- Create the genres table if it doesn't exist
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL
);

-- Create the movie_genres table if it doesn't exist
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
        ON DELETE CASCADE
);

-- Create the vectors table if it doesn't exist
CREATE TABLE IF NOT EXISTS vectors (
    movie_id INT PRIMARY KEY REFERENCES movies(movie_id),
    vec_0 FLOAT NOT NULL,
    vec_1 FLOAT NOT NULL,
    vec_2 FLOAT NOT NULL,
    vec_3 FLOAT NOT NULL,
    vec_4 FLOAT NOT NULL,
    vec_5 FLOAT NOT NULL,
    vec_6 FLOAT NOT NULL,
    vec_7 FLOAT NOT NULL,
    vec_8 FLOAT NOT NULL,
    vec_9 FLOAT NOT NULL,
    vec_10 FLOAT NOT NULL,
    vec_11 FLOAT NOT NULL,
    vec_12 FLOAT NOT NULL,
    vec_13 FLOAT NOT NULL,
    vec_14 FLOAT NOT NULL,
    vec_15 FLOAT NOT NULL,
    vec_16 FLOAT NOT NULL,
    vec_17 FLOAT NOT NULL,
    vec_18 FLOAT NOT NULL,
    vec_19 FLOAT NOT NULL,
    vec_20 FLOAT NOT NULL,
    vec_21 FLOAT NOT NULL,
    vec_22 FLOAT NOT NULL,
    vec_23 FLOAT NOT NULL,
    vec_24 FLOAT NOT NULL,
    vec_25 FLOAT NOT NULL,
    vec_26 FLOAT NOT NULL,
    vec_27 FLOAT NOT NULL,
    vec_28 FLOAT NOT NULL,
    vec_29 FLOAT NOT NULL,
    vec_30 FLOAT NOT NULL,
    vec_31 FLOAT NOT NULL,
    vec_32 FLOAT NOT NULL,
    vec_33 FLOAT NOT NULL,
    vec_34 FLOAT NOT NULL,
    vec_35 FLOAT NOT NULL,
    vec_36 FLOAT NOT NULL,
    vec_37 FLOAT NOT NULL,
    vec_38 FLOAT NOT NULL,
    vec_39 FLOAT NOT NULL,
    vec_40 FLOAT NOT NULL,
    vec_41 FLOAT NOT NULL,
    vec_42 FLOAT NOT NULL,
    vec_43 FLOAT NOT NULL,
    vec_44 FLOAT NOT NULL,
    vec_45 FLOAT NOT NULL,
    vec_46 FLOAT NOT NULL,
    vec_47 FLOAT NOT NULL,
    vec_48 FLOAT NOT NULL,
    vec_49 FLOAT NOT NULL,
    vec_50 FLOAT NOT NULL,
    vec_51 FLOAT NOT NULL,
    vec_52 FLOAT NOT NULL,
    vec_53 FLOAT NOT NULL,
    vec_54 FLOAT NOT NULL,
    vec_55 FLOAT NOT NULL,
    vec_56 FLOAT NOT NULL,
    vec_57 FLOAT NOT NULL,
    vec_58 FLOAT NOT NULL,
    vec_59 FLOAT NOT NULL,
    vec_60 FLOAT NOT NULL,
    vec_61 FLOAT NOT NULL,
    vec_62 FLOAT NOT NULL,
    vec_63 FLOAT NOT NULL,
    vec_64 FLOAT NOT NULL,
    vec_65 FLOAT NOT NULL,
    vec_66 FLOAT NOT NULL,
    vec_67 FLOAT NOT NULL,
    vec_68 FLOAT NOT NULL,
    vec_69 FLOAT NOT NULL,
    vec_70 FLOAT NOT NULL,
    vec_71 FLOAT NOT NULL,
    vec_72 FLOAT NOT NULL,
    vec_73 FLOAT NOT NULL,
    vec_74 FLOAT NOT NULL,
    vec_75 FLOAT NOT NULL,
    vec_76 FLOAT NOT NULL,
    vec_77 FLOAT NOT NULL,
    vec_78 FLOAT NOT NULL,
    vec_79 FLOAT NOT NULL,
    vec_80 FLOAT NOT NULL,
    vec_81 FLOAT NOT NULL,
    vec_82 FLOAT NOT NULL,
    vec_83 FLOAT NOT NULL,
    vec_84 FLOAT NOT NULL,
    vec_85 FLOAT NOT NULL,
    vec_86 FLOAT NOT NULL,
    vec_87 FLOAT NOT NULL,
    vec_88 FLOAT NOT NULL,
    vec_89 FLOAT NOT NULL,
    vec_90 FLOAT NOT NULL,
    vec_91 FLOAT NOT NULL,
    vec_92 FLOAT NOT NULL,
    vec_93 FLOAT NOT NULL,
    vec_94 FLOAT NOT NULL,
    vec_95 FLOAT NOT NULL,
    vec_96 FLOAT NOT NULL,
    vec_97 FLOAT NOT NULL,
    vec_98 FLOAT NOT NULL,
    vec_99 FLOAT NOT NULL,
    vec_100 FLOAT NOT NULL,
    vec_101 FLOAT NOT NULL,
    vec_102 FLOAT NOT NULL,
    vec_103 FLOAT NOT NULL,
    vec_104 FLOAT NOT NULL,
    vec_105 FLOAT NOT NULL,
    vec_106 FLOAT NOT NULL,
    vec_107 FLOAT NOT NULL,
    vec_108 FLOAT NOT NULL,
    vec_109 FLOAT NOT NULL,
    vec_110 FLOAT NOT NULL,
    vec_111 FLOAT NOT NULL,
    vec_112 FLOAT NOT NULL,
    vec_113 FLOAT NOT NULL,
    vec_114 FLOAT NOT NULL,
    vec_115 FLOAT NOT NULL,
    vec_116 FLOAT NOT NULL,
    vec_117 FLOAT NOT NULL,
    vec_118 FLOAT NOT NULL,
    vec_119 FLOAT NOT NULL,
    vec_120 FLOAT NOT NULL,
    vec_121 FLOAT NOT NULL,
    vec_122 FLOAT NOT NULL,
    vec_123 FLOAT NOT NULL,
    vec_124 FLOAT NOT NULL,
    vec_125 FLOAT NOT NULL,
    vec_126 FLOAT NOT NULL,
    vec_127 FLOAT NOT NULL,
    vec_128 FLOAT NOT NULL,
    vec_129 FLOAT NOT NULL,
    vec_130 FLOAT NOT NULL,
    vec_131 FLOAT NOT NULL,
    vec_132 FLOAT NOT NULL,
    vec_133 FLOAT NOT NULL,
    vec_134 FLOAT NOT NULL,
    vec_135 FLOAT NOT NULL,
    vec_136 FLOAT NOT NULL,
    vec_137 FLOAT NOT NULL,
    vec_138 FLOAT NOT NULL,
    vec_139 FLOAT NOT NULL,
    vec_140 FLOAT NOT NULL,
    vec_141 FLOAT NOT NULL,
    vec_142 FLOAT NOT NULL,
    vec_143 FLOAT NOT NULL,
    vec_144 FLOAT NOT NULL,
    vec_145 FLOAT NOT NULL,
    vec_146 FLOAT NOT NULL,
    vec_147 FLOAT NOT NULL,
    vec_148 FLOAT NOT NULL,
    vec_149 FLOAT NOT NULL,
    vec_150 FLOAT NOT NULL,
    vec_151 FLOAT NOT NULL,
    vec_152 FLOAT NOT NULL,
    vec_153 FLOAT NOT NULL,
    vec_154 FLOAT NOT NULL,
    vec_155 FLOAT NOT NULL,
    vec_156 FLOAT NOT NULL,
    vec_157 FLOAT NOT NULL,
    vec_158 FLOAT NOT NULL,
    vec_159 FLOAT NOT NULL,
    vec_160 FLOAT NOT NULL,
    vec_161 FLOAT NOT NULL,
    vec_162 FLOAT NOT NULL,
    vec_163 FLOAT NOT NULL,
    vec_164 FLOAT NOT NULL,
    vec_165 FLOAT NOT NULL,
    vec_166 FLOAT NOT NULL,
    vec_167 FLOAT NOT NULL,
    vec_168 FLOAT NOT NULL,
    vec_169 FLOAT NOT NULL,
    vec_170 FLOAT NOT NULL,
    vec_171 FLOAT NOT NULL,
    vec_172 FLOAT NOT NULL,
    vec_173 FLOAT NOT NULL,
    vec_174 FLOAT NOT NULL,
    vec_175 FLOAT NOT NULL,
    vec_176 FLOAT NOT NULL,
    vec_177 FLOAT NOT NULL,
    vec_178 FLOAT NOT NULL,
    vec_179 FLOAT NOT NULL,
    vec_180 FLOAT NOT NULL,
    vec_181 FLOAT NOT NULL,
    vec_182 FLOAT NOT NULL,
    vec_183 FLOAT NOT NULL,
    vec_184 FLOAT NOT NULL,
    vec_185 FLOAT NOT NULL,
    vec_186 FLOAT NOT NULL,
    vec_187 FLOAT NOT NULL,
    vec_188 FLOAT NOT NULL,
    vec_189 FLOAT NOT NULL,
    vec_190 FLOAT NOT NULL,
    vec_191 FLOAT NOT NULL,
    vec_192 FLOAT NOT NULL,
    vec_193 FLOAT NOT NULL,
    vec_194 FLOAT NOT NULL,
    vec_195 FLOAT NOT NULL,
    vec_196 FLOAT NOT NULL,
    vec_197 FLOAT NOT NULL,
    vec_198 FLOAT NOT NULL,
    vec_199 FLOAT NOT NULL,
    vec_200 FLOAT NOT NULL,
    vec_201 FLOAT NOT NULL,
    vec_202 FLOAT NOT NULL,
    vec_203 FLOAT NOT NULL,
    vec_204 FLOAT NOT NULL,
    vec_205 FLOAT NOT NULL,
    vec_206 FLOAT NOT NULL,
    vec_207 FLOAT NOT NULL,
    vec_208 FLOAT NOT NULL,
    vec_209 FLOAT NOT NULL,
    vec_210 FLOAT NOT NULL,
    vec_211 FLOAT NOT NULL,
    vec_212 FLOAT NOT NULL,
    vec_213 FLOAT NOT NULL,
    vec_214 FLOAT NOT NULL,
    vec_215 FLOAT NOT NULL,
    vec_216 FLOAT NOT NULL,
    vec_217 FLOAT NOT NULL,
    vec_218 FLOAT NOT NULL,
    vec_219 FLOAT NOT NULL,
    vec_220 FLOAT NOT NULL,
    vec_221 FLOAT NOT NULL,
    vec_222 FLOAT NOT NULL,
    vec_223 FLOAT NOT NULL,
    vec_224 FLOAT NOT NULL,
    vec_225 FLOAT NOT NULL,
    vec_226 FLOAT NOT NULL,
    vec_227 FLOAT NOT NULL,
    vec_228 FLOAT NOT NULL,
    vec_229 FLOAT NOT NULL,
    vec_230 FLOAT NOT NULL,
    vec_231 FLOAT NOT NULL,
    vec_232 FLOAT NOT NULL,
    vec_233 FLOAT NOT NULL,
    vec_234 FLOAT NOT NULL,
    vec_235 FLOAT NOT NULL,
    vec_236 FLOAT NOT NULL,
    vec_237 FLOAT NOT NULL,
    vec_238 FLOAT NOT NULL,
    vec_239 FLOAT NOT NULL,
    vec_240 FLOAT NOT NULL,
    vec_241 FLOAT NOT NULL,
    vec_242 FLOAT NOT NULL,
    vec_243 FLOAT NOT NULL,
    vec_244 FLOAT NOT NULL,
    vec_245 FLOAT NOT NULL,
    vec_246 FLOAT NOT NULL,
    vec_247 FLOAT NOT NULL,
    vec_248 FLOAT NOT NULL,
    vec_249 FLOAT NOT NULL,
    vec_250 FLOAT NOT NULL,
    vec_251 FLOAT NOT NULL,
    vec_252 FLOAT NOT NULL,
    vec_253 FLOAT NOT NULL,
    vec_254 FLOAT NOT NULL,
    vec_255 FLOAT NOT NULL
);
