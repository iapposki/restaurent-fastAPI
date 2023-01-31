/*
  Warnings:

  - The primary key for the `StoreStatus` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "StoreStatus" DROP CONSTRAINT "StoreStatus_pkey",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "StoreStatus_pkey" PRIMARY KEY ("id");
