def stop(line):
    if  'cbb' in line or 'nf' in line or 'nep' in line or 'di' in line or 'shi' in line or 'v_2' in line or 'ahref' in line or 'da' in line or '(t)' in line or '(de)' in line or '(neu)' in line or 'category' in line or '(d)' in line or '(p)' in line or '(nh)' in line or '(caa)' in line or '(dfa)' in line or '(ncd)' in line or '(b)' in line or 'g(fw)' in line:
        return True
    else:
        return False

def stop2(line):
    if  'cbb' in line or 'nf' in line or 'nep' in line or 'di' in line or 'shi' in line or 'v_2' in line or 'ahref' in line or 'da' in line or 't' in line or 'de' in line or 'category' in line or 'd' in line or 'p' in line or 'nh' in line or 'caa' in line or 'ncd' in line:
        return True
    else:
        return False

stopAttr = {'QUESTIONCATEGORY':True,
            'ETCCATEGORY':True,
            'V_2':True,
            'I':True,
            'b':True,
            'SEMICOLONCATEGORY':True,
            'COLONCATEGORY':True,
            'Cbb':True,
            'Caa':True,
            'SHI':True,
            'T':True,
            'P':True,
            'COMMACATEGORY':True,
            'EXCLAMATIONCATEGORY':True,
            'Cab':True,
            'Dfb':True,
            'Neqb':True,
            'PERIODCATEGORY':True,
            'Di':True,
            'Dk':True,
            'PAUSECATEGORY':True,
            'Nep':True,
            'Ng':True,
            'FW':True,
            'Nv':True,
            'Nh':True,
            'DE':True,
            'D':True,
            'Nf':True,
            'PARENTHESISCATEGORY':True,
            'Nes':True,
            'DASHCATEGORY':True,
            'FW':True
            }
def stop3(termAttr):
    if  stopAttr.has_key(termAttr):
        return True
    else:
        return False