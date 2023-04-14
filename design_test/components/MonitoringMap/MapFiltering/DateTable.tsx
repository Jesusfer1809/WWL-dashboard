import React, { useState } from "react";
import Datepicker from "react-tailwindcss-datepicker"; 



import {BsCalendarDay} from "react-icons/bs"
import moment from "moment";
import { useMonitoringMapStateStore } from "@/store/MonitoringMapStateStore";

function DateTable() {

    const date = useMonitoringMapStateStore((state) => state.date);
    const changeDate = useMonitoringMapStateStore((state) => state.changeDate);

    const value = { 
        startDate: date, 
        endDate: date
    }

  return (
    <div className='grid grid-cols-1 md:grid-cols-2 gap-x-8 xl:gap-x-10'>
        <div className='flex flex-col gap-y-1'>
            <h3 className=' text-xs font-semibold'>Date</h3>

            <Datepicker 
                inputClassName="py-4 rounded-xl dark:bg-[#222222]"
                
                useRange={false} 
                asSingle={true} 
                // showShortcuts={true} 
                // showFooter={true} 
                primaryColor={"orange"} 
                value={value} 
                onChange={(value)=>{
                    console.log(value);
                    
                    if(!value || value.startDate === null) return changeDate(moment(Date.now()).format("YYYY-MM-DD"))
                    //@ts-ignore
                    changeDate(value.startDate)
                }} 
                displayFormat={"MMM DD YYYY"} 
                readOnly={true} 
                /> 
            
            
        </div>
    </div>
  )
}

export default DateTable