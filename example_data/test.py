from pyclmuapp import usp_clmu
import matplotlib.pyplot as plt

def test_usp_clmu_basic():
    usp = usp_clmu()

    usp_london = usp.run(
                case_name = "example1", 
                SURF="surfdata.nc",
                FORCING="forcing.nc",
                RUN_STARTDATE = "2012-01-01",
                STOP_OPTION = "ndays", 
                STOP_N = "2"
            )
    print("Result from udocker container:")
    print(usp_london)
    print("cleaning up case example1...")
    usp.case_clean(case_name="example1")

def test_usp_clmu_udocker():
    try:
        import udocker
        print("You are using udocker container.")
        usp = usp_clmu(container_type="udocker")

        usp_london = usp.run(
                    case_name = "example1", 
                    SURF="surfdata.nc",
                    FORCING="forcing.nc",
                    RUN_STARTDATE = "2012-01-01",
                    STOP_OPTION = "ndays", 
                    STOP_N = "2"
                )

        print("Result from udocker container:")
        print(usp_london)
        print("cleaning up case example1...")
        usp.case_clean(case_name="example1")
    except ImportError:
        raise ImportError("You don't have udocker installed. Please install udocker if you want to use udocker container.")
    
if __name__ == "__main__":
    test_usp_clmu_basic()
    import os
    if os.name == 'posix':
        test_usp_clmu_udocker()