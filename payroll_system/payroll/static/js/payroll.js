document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('id_time_in').addEventListener('change', calculateTotalHours);
    document.getElementById('id_time_out').addEventListener('change', calculateTotalHours);

    function calculateTotalHours() {
        const timeIn = document.getElementById('id_time_in').value;
        const timeOut = document.getElementById('id_time_out').value;

        if (timeIn && timeOut) {
            const timeInDate = new Date(timeIn);
            const timeOutDate = new Date(timeOut);

            const diffMillis = timeOutDate - timeInDate;

            if (diffMillis > 0) {
                const hoursWorked = Math.floor(diffMillis / 1000 / 60 / 60);
                document.getElementById('total_hours_worked').value = hoursWorked;
                updateSalaryCalculations();
            } else {
                document.getElementById('total_hours_worked').value = 0;
            }
        }
    }

    // Function to update subtotal and net salary
    function updateSalaryCalculations() {
        const dailyRate = parseFloat(document.getElementById("id_daily_rate").value) || 0;
        const totalHours = parseFloat(document.getElementById("total_hours_worked").value) || 0;
        const nightDiff = parseFloat(document.getElementById("id_night_differential_hour").value) || 0;
        const deductions = parseFloat(document.getElementById("id_deductions").value) || 0;
        const overtimeHour = parseFloat(document.getElementById("id_overtime_hour").value) || 0;
        const allowance = parseFloat(document.getElementById("id_allowance").value) || 0;
        
        // Calculate Breaktime
        let netHour = totalHours >= 10 ? 8 : totalHours;
        let breakHour = 1;
        if (netHour == 8 && totalHours >= 10) {
            breakHour = 0;
        } else if (netHour >= 6) {
            breakHour = 2;
        }

        let netOt = ((dailyRate / 8) * 1.25) * overtimeHour;
        let netNightDiff = ((dailyRate / 8) * 0.1) * nightDiff;
        const hourlyRate = dailyRate / 8;
        const subtotal = (hourlyRate * (netHour - breakHour)) + netOt + netNightDiff + allowance;
        const netSalary = subtotal - deductions;
        
        if (totalHours > 0) {
            document.getElementById('subtotal').value = subtotal.toFixed(2);
            document.getElementById('net_salary').value = netSalary.toFixed(2);
        } else {
            document.getElementById('subtotal').value = 0;
            document.getElementById('net_salary').value = 0;
        }
        document.getElementById('overtime_pay').value = netOt.toFixed(2);
        document.getElementById('night_differential_pay').value = netNightDiff.toFixed(2);
    }

    // Add event listeners to the relevant input fields
    document.getElementById("id_daily_rate").addEventListener("input", updateSalaryCalculations);
    document.getElementById("id_overtime_hour").addEventListener("input", updateSalaryCalculations);
    document.getElementById("id_night_differential_hour").addEventListener("input", updateSalaryCalculations);
    document.getElementById("id_deductions").addEventListener("input", updateSalaryCalculations);
    document.getElementById("id_allowance").addEventListener("input", updateSalaryCalculations);
    
});
