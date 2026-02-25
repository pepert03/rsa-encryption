"""
imatlab_benchmark.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Description:
Script to measure execution times for the IMAT-LAB program.

Usage instructions:
Edit the input/output file lists to run different benchmarks.

The main loop contains code to run benchmarking and/or profiling using each of the
provided input files. Comment out whichever part you don't need.
"""

import timeit
import cProfile
import imatlab

# Number of repetitions.
# Increasing it reduces random noise, but increases total execution time.
NITERS=100

def testRun(in_file:str, out_file:str):
    """Wrapper for timeit/profile.

    Opens the provided files and executes their commands using the imatlab module.
    
    Args:
        in_file: Nombre del fichero de entrada.
        out_file: Nombre del fichero de salida.
    
    Returns: Void
    Raises:
        IOError: Alguno de los ficheros no existe.
    """
    with open(in_file,"r") as fin:
        with open(out_file,"w",encoding="utf-8") as fout:
            imatlab.run_commands(fin,fout)

def measureTime(in_file:str,out_file:str)->float:
    """Measure average runtime of imatlab using the provided files.

    Args:
        in_file: Nombre del fichero de entrada.
        out_file: Nombre del fichero de salida.
    
    Returns:
        float: Tiempo de ejecución medio medido
    Raises:
        IOError: Alguno de los ficheros no existe.
    """
    t=timeit.Timer("testRun('"+in_file+"','"+out_file+"')","from __main__ import testRun")
    return(t.timeit(number=NITERS)/NITERS)

def profile(in_file,out_file):
    """Print a profile of imatlab execution for the provided files.

    Args:
        in_file: Nombre del fichero de entrada.
        out_file: Nombre del fichero de salida.
    
    Returns: Void
    Raises:
        IOError: Alguno de los ficheros no existe.
    """
    cProfile.run("testRun('"+in_file+"','"+out_file+"')")



if __name__ == "__main__":
    # Initialize input/output file lists to process.
    # Comment/add/remove files as needed.
    #in_files=["primosTest.txt","factorTest.txt","mcdTest.txt","potenciaTest.txt",
    #            "invTest.txt","eulerTest.txt","sistemaTest.txt","cuadraticaTest.txt"]
    #out_files=["primosTest_out.txt","factorTest_out.txt","mcdTest_out.txt","potenciaTest_out.txt",
    #            "invTest_out.txt","eulerTest_out.txt","sistemaTest_out.txt","cuadraticaTest_out.txt"]
    in_files=["ejemplosComandos.txt"]
    out_files=["ejemplosSalida.txt"]
    
    # Collected timings
    runtime=[]
    for i in range(0,len(in_files)):
        # Comment one line or the other to switch benchmarking/profiling
        try:
            runtime.append(measureTime(in_files[i],out_files[i]))
        #    profile(in_files[i],out_files[i])
        except IOError:
            runtime.append(0)
            print("File "+in_files[i]+" does not exist.\n")

    print(runtime)