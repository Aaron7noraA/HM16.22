import os
import sys
import argparse
from tqdm import tqdm
from subprocess import Popen, PIPE
from Setting import DATASET, QP
from concurrent.futures import ProcessPoolExecutor, as_completed

def runHMcodec(codingCfg: str, seqCfg: str, outName: str) -> None:
    command = f"./EncoderAppStatic -c {codingCfg} -c {seqCfg} > {outName}"
    return command

def run_command(command: str):
    process = Popen(command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE)
    status = process.wait()
    return command

def main(argv):   

    parser = argparse.ArgumentParser(description="Set the root of dataset and for save")
    parser.add_argument('--codingCfg', type=str, required=True, help="Path of cfg/encoder_lowdelay_vtm.cfg")
    parser.add_argument('--cfgRoot', type=str, required=True, help="Path for save the cfg files and results")
    parser.add_argument('--taskMax', type=int, required=True, help="MAX compress sequence at the same time, recommended to be less than CPU core number.")
    args = parser.parse_args(argv)

    datasets = DATASET

    qpValues = QP
    # qp = [27, 32, 37]

    qpProcesses = []
    for qp in qpValues:
        for datasetName, seqs in datasets.items():
            for seqName, seq in seqs.items():
                cfgPath = os.path.join(args.cfgRoot, datasetName, f"qp={qp}", seqName)
                width, height = seq["frameWH"]
                # name = seq['vi_name']
                if datasetName in ['HEVC-C', 'HEVC-D', 'HEVC-E', 'HEVC-RGB']:
                    name = seq["vi_name"]
                else:
                    name = f"{seqName}_1920x1080_{seq['frameRate']}" 

                cfgName = os.path.join(cfgPath, name + '.cfg')
                outName = os.path.join(cfgPath, name + '.out')
                qpProcesses.append(runHMcodec(args.codingCfg, cfgName, outName))

    with tqdm(total=len(qpProcesses), unit='seq', desc='seqs') as pbar:
        with ProcessPoolExecutor(max_workers=args.taskMax) as executor:
            futures = {executor.submit(run_command, single_command): single_command for single_command in qpProcesses}
            for future in as_completed(futures):
                command = futures[future]
                try:
                    result = future.result()
                    tqdm.write(f'Command "{result}" completed')
                except Exception as e:
                    tqdm.write(f'Command "{command}" generated an exception: {e}')
                pbar.update(1)

if __name__ == "__main__":
    main(sys.argv[1:])