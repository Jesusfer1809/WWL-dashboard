import React from "react";
import { AiOutlineUser } from "react-icons/ai";
import { BsArrowDownUp, BsTrash } from "react-icons/bs";
import { ReportDetails } from "../../types";
import moment from "moment";
import { Link } from "react-router-dom";

function ReportsListTable({ reports }: { reports: ReportDetails[] }) {
  return (
    <div
      className={`max-w-[1000vh] h-[21rem] sm:h-[24.5rem] md:h-[28rem] overflow-x-auto rounded-lg border-2 bg-white border-[#333]`}
    >
      <table className=" select-none w-full border-collapse bg-white">
        <thead>
          <tr
            className={`w-full flex items-center px-8 whitespace-nowrap  gap-x-10 md:gap-x-12 justify-evenly  h-14  font-medium text-white bg-[#333]`}
          >
            <th className="flex items-center gap-x-2 w-36 md:w-10 justify-center ">
              <span className="text-[11px] md:text-xs">N°</span>
              <BsArrowDownUp className="w-2" />
            </th>

            <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center ">
              <span className="text-[11px] md:text-xs">Created by</span>
              <BsArrowDownUp className="w-2" />
            </th>

            <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center">
              <span className="text-[11px] md:text-xs">Report title</span>
              <BsArrowDownUp className="w-2" />
            </th>

            <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center">
              <span className="text-[11px] md:text-xs">Report description</span>
              <BsArrowDownUp className="w-2" />
            </th>

            <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center">
              <span className="text-[11px] md:text-xs">Piezo. location</span>
              <BsArrowDownUp className="w-2" />
            </th>

            <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center"></th>

            <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center"></th>
            <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center"></th>
          </tr>
        </thead>

        <tbody className="bg-white">
          {reports.map((report, i) => (
            <tr key={report.report_id} style={{
              backgroundColor: i%2===0 ? "#dfdfdf" : "white"
            }} className="w-full flex items-center justify-evenly whitespace-nowrap gap-x-14 md:gap-x-16 px-8  text-[9px] md:text-[10px] h-14 bg-white ">
              <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center">
                <span className="text-xs">{String(i+1).padStart(2,"0")}.</span>
              </th>

              <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center">
                <div className="w-6 h-6 border border-[#333] rounded-full flex items-center justify-center">
                  <img src={`/media/img/photos/${report.user_picture}`} />
                </div>
                <span>{report.user_name}</span>
              </th>

              <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center ">
                <span>{report.report_title}</span>
              </th>

              <th className="flex items-center gap-x-2 w-36 md:w-40 justify-center">
                <span>{moment(report.report_date).format("MMM DD, YYYY")}</span>
              </th>

              <th className="flex items-center gap-x-1 w-36 md:w-40 justify-center">
                <span>
                  {report.report_paddock} 
                </span>
                <span>
                  /
                </span>

                <span>
                {report.report_piezo}
                </span>
              </th>

              <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center">
                <Link to={`/reports/piezometers/${report.report_id}`}>
                <span className="text-[11px] md:text-xs text-cyan-600 border-b-2 border-cyan-600  hover:text-cyan-800 hover:border-cyan-800 transition-all cursor-pointer">
                  View
                </span>
                
                </Link>
              </th>

              <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center">
                <span className="text-[11px] md:text-xs text-cyan-600 border-b-2 border-cyan-600  hover:text-cyan-800 hover:border-cyan-800 transition-all cursor-pointer">
                  Edit
                </span>
              </th>
              <th className="flex items-center gap-x-2 w-8 md:w-10 justify-center">
                <div className=" w-7 h-7 md:w-9 md:h-9 bg-damaged-normal hover:bg-opacity-40 transition-all cursor-pointer  bg-opacity-30 rounded-full flex items-center justify-center">
                  <BsTrash className="h-3 w-3 md:w-4 md:h-4 text-damaged-dark" />
                </div>
              </th>
            </tr>
          ))}
          
        </tbody>
      </table>
    </div>
  );
}

export default ReportsListTable;
