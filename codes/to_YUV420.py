import os
import numpy as np
import argparse

dataset = {
    'UVG': ['Beauty_1920x1080_120.yuv', 'Bosphorus_1920x1080_120.yuv', 
            'HoneyBee_1920x1080_120.yuv', 'Jockey_1920x1080_120.yuv', 
            'ReadySteadyGo_1920x1080_120.yuv', 'ShakeNDry_1920x1080_120.yuv',
            'YachtRide_1920x1080_120.yuv'],

    # 'HEVC-B': ['BasketballDrive_1920x1080_50.yuv', 'BQTerrace_1920x1080_60.yuv',
    #            'Cactus_1920x1080_50.yuv', 'Kimono1_1920x1080_24.yuv',
    #            'ParkScene_1920x1080_24.yuv']
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Set the root of dataset and for save")
    parser.add_argument('--datasetRoot', type=str, default="/home/pc3447/Datasets/")
    parser.add_argument('--saveRoot', type=str, required=True)
    args = parser.parse_args()

    args.datasetRoot = os.path.abspath(args.datasetRoot)
    args.saveRoot = os.path.abspath(args.saveRoot)

    shape = (1080, 1920)
    k = 1920 * 1080 * 3
    size = np.prod(shape)

    for ds in dataset.keys():
        # source_root = f'../{ds}_YUV420'
        source_root = os.path.join(args.datasetRoot, ds)
        # save_root = f'../{ds}_YUV400'
        save_root = os.path.join(args.datasetRoot, f'{ds}_YUV420')
        os.makedirs(save_root, exist_ok=True)

        for seq in dataset[ds]:
            source_path = os.path.join(source_root, seq)
            dest_path = os.path.join(save_root, seq)
            print(source_path)
            source = open(source_path, 'rb')
            with open(dest_path, 'wb') as dest:
                print(k)
                assert os.path.getsize(source_path) % k == 0, f"This {source_path} may not in YUV444 format"
                num_frames = os.path.getsize(source_path) // (shape[0] * shape[1])
                for _ in range(num_frames):
                    Y = source.read(size)
                    
                    U = source.read(size)
                    U = np.frombuffer(U, dtype=np.uint8).copy().reshape(1, shape[0], shape[1])[:, ::2, ::2].tobytes()

                    V = source.read(size)
                    V = np.frombuffer(V, dtype=np.uint8).copy().reshape(1, shape[0], shape[1])[:, ::2, ::2].tobytes()
                    print(V.size)
                    exit()

                    dest.write(Y)
                    dest.write(U)
                    dest.write(V)
            
            source.close()