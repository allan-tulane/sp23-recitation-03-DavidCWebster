"""
CMPS 2200  Recitation 3.
See recitation-03.pdf for details.
"""
import time


class BinaryNumber:
  """ done """

  def __init__(self, n):
    self.decimal_val = n
    self.binary_vec = list('{0:b}'.format(n))

  def __repr__(self):
    return ('decimal=%d binary=%s' %
            (self.decimal_val, ''.join(self.binary_vec)))


## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.


def binary2int(binary_vec):
  if len(binary_vec) == 0:
    return BinaryNumber(0)
  return BinaryNumber(int(''.join(binary_vec), 2))


def split_number(vec):
  return (binary2int(vec[:len(vec) // 2]), binary2int(vec[len(vec) // 2:]))


def bit_shift(number, n):
  # append n 0s to this number's binary string
  return binary2int(number.binary_vec + ['0'] * n)


def pad(x, y):
  # pad with leading 0 if x/y have different number of bits
  # e.g., [1,0] vs [1]
  if len(x) < len(y):
    x = ['0'] * (len(y) - len(x)) + x
  elif len(y) < len(x):
    y = ['0'] * (len(x) - len(y)) + y
  # pad with leading 0 if not even number of bits
  if len(x) % 2 != 0:
    x = ['0'] + x
    y = ['0'] + y
  return x, y


def _quadratic_multiply(x, y):

  #xvec=BinaryNumber(x)
  #yvec=BinaryNumber(y)

  xvec = x
  yvec = y

  #pad both numbers so that we can split them evenly later
  xvec.binary_vec, yvec.binary_vec = pad(xvec.binary_vec, yvec.binary_vec)

  #basic returns for the values of 1 and 0
  if xvec.decimal_val == 1:
    return yvec
  if yvec.decimal_val == 1:
    return xvec

  if xvec.decimal_val == 0:
    yvec.decimal_val = 0
    yvec.binary_value = [0]
    return yvec
  if yvec.decimal_val == 0:
    yvec.decimal_val = 0
    yvec.binary_value = [0]
    return yvec

  #split the binary vectors in half, then convert them into binry numbers
  xvecLeft = xvec.binary_vec[:len(xvec.binary_vec) // 2]
  xvecLeft = binary2int(xvecLeft)

  xvecRight = xvec.binary_vec[len(xvec.binary_vec) // 2:]
  xvecRight = binary2int(xvecRight)

  yvecLeft = xvec.binary_vec[:len(yvec.binary_vec) // 2]
  yvecLeft = binary2int(yvecLeft)

  yvecRight = xvec.binary_vec[len(yvec.binary_vec) // 2:]
  yvecRight = binary2int(yvecRight)

  #n which will be used to know how much to bit shift by
  n = len(xvec.binary_vec)

  # (2^n)(xL · yL) part of the sum
  firstSection = bit_shift(_quadratic_multiply(xvecLeft, yvecLeft), n)

  # (xL · yR) + (xR · yL) part of the sum
  # since we have to add we call decimal_val
  inner = _quadratic_multiply(xvecLeft,
                              yvecRight).decimal_val + _quadratic_multiply(
                                xvecRight, yvecLeft).decimal_val

  # convert inner from decimal into Binary number
  inner2 = BinaryNumber(inner)

  #bit shifts the inner part to get the complete second part of the summation
  secondSection = bit_shift(inner2, n // 2)

  #third part of the summation
  thirdSection = _quadratic_multiply(xvecRight, yvecRight)

  #to add call decimal_val, then convert back into a Binary Number
  return BinaryNumber(firstSection.decimal_val + secondSection.decimal_val +
                      thirdSection.decimal_val)


def quadratic_multiply(x, y):

  return _quadratic_multiply(x, y).decimal_val


## Feel free to add your own tests here.
def test_multiply():
  assert quadratic_multiply(BinaryNumber(2), BinaryNumber(2)) == 2 * 2


def time_multiply(x, y, f):
  start = time.time()
  # multiply two numbers x, y using function f
  return (time.time() - start) * 1000
