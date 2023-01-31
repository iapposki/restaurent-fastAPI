-- CreateTable
CREATE TABLE "StoreStatus" (
    "store_id" INTEGER NOT NULL,
    "timestamp_utc" TIMESTAMP(3) NOT NULL,
    "status" TEXT NOT NULL,

    CONSTRAINT "StoreStatus_pkey" PRIMARY KEY ("store_id")
);

-- CreateTable
CREATE TABLE "StoreHours" (
    "store_id" INTEGER NOT NULL,
    "day_of_week" INTEGER,
    "start_time_local" TIMESTAMP(3),
    "end_time_local" TIMESTAMP(3),

    CONSTRAINT "StoreHours_pkey" PRIMARY KEY ("store_id")
);

-- CreateTable
CREATE TABLE "StoreTimeZone" (
    "store_id" INTEGER NOT NULL,
    "timezone_str" TEXT NOT NULL,

    CONSTRAINT "StoreTimeZone_pkey" PRIMARY KEY ("store_id")
);
