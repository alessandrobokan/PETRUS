def case1(w, p, p0, pVt, k, c):
    w = w[:p[k] + 1] + '-' + w[p[k] + 1:]
    p0 = p[k] + 1
    k = k + 1 if k + 1 < len(p) else k
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case2(w, p, p0, pVt, k, c):
    w = w[:p[k] + 2] + '-' + w[p[k] + 2:]
    p0 = p[k] + 2
    k = k + 1 if k + 1 < len(p) else k
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case3(w, p, p0, pVt, k, c):
    w = w[:p[k] + 1] + '-' + w[p[k] + 1:]
    p0 = p[k] + 1
    k += 1
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case4(w, p, p0, pVt, k, c):
    w = w[:p[k] + 2] + '-' + w[p[k] + 2:]
    p0 = p[k] + 2
    k = k + 1 if k + 1 < len(p) else k
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case5(w, p, p0, pVt, k, c):
    w = w[:p[k] + 3] + '-' + w[p[k] + 3:]  # Case 5
    p0 = p[k] + 3
    k += 1
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case6(w, p0):
    p0 += len(w) - 1
    return p0


def case7(w, p, p0, pVt, k, c):
    w = w[:p[k] + 3] + '-' + w[p[k] + 3:]  # Case 5
    p0 = p[k] + 3
    k += 1
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case8(w, p, p0, pVt, k, c):
    w = w[:p[k] + 1] + '-' + w[p[k] + 1:]
    p0 = p[k] + 1
    k += 1
    c += 1
    p[k] = p[k] + c
    pVt += 1
    return w, p0, k, c, p, pVt


def case9(w, p, p0, pVt, k, c):
    w = w[:p0 + 1] + '-' + w[p0 + 1:]
    p0 += 1
    k = k
    c += 1
    p[k] = p[k] + 1
    pVt += 1
    return w, p0, k, c, p, pVt


def case10(w, p, p0, pVt, k, c):
    w = w[:p0 + 2] + '-' + w[p0 + 2:]
    p0 += 2
    k = k
    c += 1
    p[k] = p[k] + 1
    pVt += 1
    return w, p0, k, c, p, pVt
