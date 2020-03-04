jti = get_raw_jwt()['jti']
        if jti in black_list:
            print jti