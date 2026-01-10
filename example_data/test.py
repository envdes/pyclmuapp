from pyclmuapp import usp_clmu
import matplotlib.pyplot as plt

usp = usp_clmu()

usp_london = usp.run(
            case_name = "example1", 
            SURF="surfdata.nc",
            FORCING="forcing.nc",
            RUN_STARTDATE = "2012-01-01",
            STOP_OPTION = "ndays", 
            STOP_N = "2"
        )

print(usp_london)