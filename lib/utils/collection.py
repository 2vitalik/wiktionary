
def chunks(items, chunk_len):
    """ Yield successive n-sized chunks from items """
    for i in range(0, len(items), chunk_len):
        yield items[i:i+chunk_len]
