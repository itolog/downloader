def progress(self, blocknum, blocksize, totalsize):
    readed_data = blocknum * blocksize

    if totalsize > 0:
        download_percentage = readed_data * 100 / totalsize
        self.progressBar.setValue(int(download_percentage))
