/*
  Warnings:

  - The primary key for the `StoreStatus` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "StoreStatus" DROP CONSTRAINT "StoreStatus_pkey",
ALTER COLUMN "store_id" SET DATA TYPE BIGINT,
ADD CONSTRAINT "StoreStatus_pkey" PRIMARY KEY ("store_id");
