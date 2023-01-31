/*
  Warnings:

  - The primary key for the `StoreHours` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "StoreHours" DROP CONSTRAINT "StoreHours_pkey",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "StoreHours_pkey" PRIMARY KEY ("id");
