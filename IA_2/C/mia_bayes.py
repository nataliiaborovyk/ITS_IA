def bayer_sequenza(sequenza, valore_a, p_a_dato_b, p_a_dato_non_b, prior):

    p_non_a_dato_b = 1 - p_a_dato_b
    p_non_a_dato_non_b = 1 - p_a_dato_non_b
    
    p_b = prior
    result = [p_b]
    for evidenza in sequenza:
        if evidenza == valore_a:
            p_a = p_a_dato_b*p_b + p_a_dato_non_b*(1-p_b)
            p_b_dato_a = (p_a_dato_b*p_b/p_a)
            p_b = p_b_dato_a
            result.append(p_b)
        else:
            p_non_a = p_non_a_dato_b*p_b + p_non_a_dato_non_b*(1-p_b) 
            p_b_dato_non_a = (p_non_a_dato_b)*p_b/p_non_a
            p_b = p_b_dato_non_a
            result.append(p_b)
    return result