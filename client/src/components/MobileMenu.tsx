import React, { useState, useEffect } from "react";
import { useMobileMenuStore } from "../store/MobileMenuStore";
import DesktopLink from "./DesktopLink";
import DesktopSubLink from "./DesktopSubLink";
import UserIDCard from "./UserIDCard";

import { AiOutlineClose } from "react-icons/ai";
import { useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";

function MobileMenu() {
  const mobileMenuIsOpen = useMobileMenuStore(
    (state) => state.mobileMenuIsOpen
  );
  const closeMobileMenu = useMobileMenuStore((state) => state.closeMobileMenu);

  const location = useLocation();

  const currentPage = location.pathname;

  // const router = useRouter();

  // useEffect(() => {
  //   setCurrentPage(router.route);
  // });
  return (
    <AnimatePresence>
      {mobileMenuIsOpen ? (
        <motion.div
          initial={{ x: "100%" }}
          animate={{
            x: "0%",
            transition: { duration: 0.7, ease: "easeInOut" },
          }}
          exit={{ x: "100%", transition: { duration: 0.7, ease: "easeInOut" } }}
          key="mobile-menu"
          className=" md:hidden fixed top-0 left-0 z-[100] h-screen w-screen bg-[#F1F5F9] py-8  px-4 overflow-scroll "
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{
              opacity: 1,
              transition: { duration: 0.5, ease: "easeInOut" },
            }}
            exit={{
              opacity: 0,
              transition: { duration: 0.5, ease: "easeInOut" },
            }}
            className="flex justify-between items-center"
          >
            <div className="w-36 relative rounded-md overflow-hidden">
              <img
                src="/static/img/rossing_logo.png"
                className="w-full object-contain"
              />
            </div>

            <div
              onClick={closeMobileMenu}
              className="p-2 border-2 border-orangeSecondaryShadow rounded-full"
            >
              <AiOutlineClose className="w-6 h-6" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{
              opacity: 1,
              transition: { duration: 0.5, ease: "easeInOut" },
            }}
            exit={{
              opacity: 0,
              transition: { duration: 0.5, ease: "easeInOut" },
            }}
            className="mt-12 flex flex-col gap-y-10"
          >
            <UserIDCard />

            <div className="flex flex-col gap-y-10 ">
              <DesktopLink
                title="Dashboard"
                icon="dashboard"
                linkTo="/"
                hasSubLinks={false}
                isCurrentPage={currentPage === "/"}
              />
              <DesktopLink
                title="Monitoring Chart"
                icon="chart"
                linkTo="/paddock-lectures"
                hasSubLinks={false}
                isCurrentPage={currentPage === "/paddock-lectures"}
              />

              <div>
                <DesktopLink
                  title="Reports"
                  icon="reports"
                  hasSubLinks={true}
                  isCurrentPage={false}
                />

                <div className="flex flex-col gap-y-6  mt-4">
                  <DesktopSubLink
                    title="Piezometers"
                    linkTo="/reports/piezometers"
                    isCurrentPage={currentPage.startsWith(
                      "/reports/piezometers"
                    )}
                  />
                  <DesktopSubLink
                    title="Incidents"
                    linkTo="/reports/incidents"
                    isCurrentPage={currentPage.startsWith("/reports/incidents")}
                  />

                  <DesktopSubLink
                    title="Visits"
                    linkTo="/biannual-visits"
                    isCurrentPage={currentPage.startsWith("/biannual-visits")}
                  />
                </div>
              </div>
              <div>
                <DesktopLink
                  title="Account"
                  icon="account"
                  hasSubLinks={true}
                  isCurrentPage={false}
                />
                <div className="flex flex-col gap-y-4  mt-4">
                  <DesktopSubLink
                    title="Log Out"
                    isAccountLogOut
                    isCurrentPage={false}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

export default MobileMenu;