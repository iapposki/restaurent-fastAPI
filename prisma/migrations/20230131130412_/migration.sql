/*
  Warnings:

  - The `start_time_local` column on the `StoreHours` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The `end_time_local` column on the `StoreHours` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- AlterTable
ALTER TABLE "StoreHours" DROP COLUMN "start_time_local",
ADD COLUMN     "start_time_local" DATE,
DROP COLUMN "end_time_local",
ADD COLUMN     "end_time_local" DATE;
