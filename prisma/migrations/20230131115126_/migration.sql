/*
  Warnings:

  - The primary key for the `StoreTimeZone` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "StoreHours" ALTER COLUMN "store_id" SET DATA TYPE BIGINT;

-- AlterTable
ALTER TABLE "StoreTimeZone" DROP CONSTRAINT "StoreTimeZone_pkey",
ALTER COLUMN "store_id" SET DATA TYPE BIGINT,
ADD CONSTRAINT "StoreTimeZone_pkey" PRIMARY KEY ("store_id");
