schtasks /create /f /tn "DashboardRO_Update_12" /tr "wscript.exe \"G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro\run_update_hidden.vbs\"" /sc daily /st 12:00
schtasks /create /f /tn "DashboardRO_Update_16" /tr "wscript.exe \"G:\My Drive\ANTIGRAVITY\Tro_Ly\dashboard-ro\run_update_hidden.vbs\"" /sc daily /st 16:00
