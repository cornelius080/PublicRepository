# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:16:38 2022

@author: gscalera


ADOPTED CONVENTIONS
- Rotation matrix <from body to earth frame> ->     q * p * q^-1
- Aerospatial Euler sequence ZYX (or 321)
- Roll e Yaw are included in the interval (-180, +180); il pitch is included betweeen (-90, +90)


USEFUL LINKS
https://en.wikipedia.org/wiki/Rotation_matrix
https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions
https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

https://eater.net/quaternions
https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToEuler/

https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
"""

import numpy as np

VersorX = np.array([1,0,0]).astype(float)
VersorY = np.array([0,1,0]).astype(float)
VersorZ = np.array([0,0,1]).astype(float)
QuatIdentity = np.array([1,0,0,0]).astype(float)


def Vec2SkewSymmetricMatrix(vec):
    """
    Takes an array of R3 in input and defines a skew symmetric matrix

    Parameters
    ----------
    vec : np.array (3,)

    Returns
    -------
    skewMat : Skew symmetric matrix 3 x 3

    """
    vec = vec.reshape((3,))
    row1 = np.array([0, -vec[2], vec[1]]).astype(float)
    row2 = np.array([vec[2], 0, -vec[0]]).astype(float)
    row3 = np.array([-vec[1], vec[0], 0]).astype(float)
    skewMat = np.row_stack((row1, row2, row3))
    return skewMat
    

def Vec2Quat(vec):
    """
    Converts the 3D array into a quaternion

    Parameters
    ----------
    vec : np.array (3,)

    Returns
    -------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    """
    vec = vec.reshape((3,))
    quat = np.concatenate((np.array([0]), vec)).astype(float)
    return quat
    

def Quat2Rotm(quat):
    """
    Converts the quaternion into a rotation matrix (from body frame to Earth frame - transpose of dcm)

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    The rotation matrix equivalent to the quaternion in the body to Earth frame
    """
    quat = quat.reshape((4,))
    
    vectorPart = quat[1:]
    scalarPart = quat[0]
    
    skewMat = Vec2SkewSymmetricMatrix(vectorPart)
    
    rotm = (scalarPart**2 - vectorPart.T @ vectorPart)*np.eye(3) + 2*np.outer(vectorPart, vectorPart) + 2*scalarPart*skewMat
    
    # Equivalente alla precedente
    # rotm2 = np.array([[1-2*(y**2+z**2), 2*(x*y - z*w), 2*(x*z + y*w)], [2*(x*y + z*w), 1-2*(x**2 + z**2), 2*(y*z -x*w)], [2*(x*z - y*w), 2*(y*z + x*w), 1-2*(x**2 + y**2)]]).astype(float)
    
    return rotm
    

def Quat2Dcm(quat):
    """
    Converts the quaternion into a rotation matrix (from Earth frame to body frame)

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    The rotation matrix equivalent to the quaternion in the Earth to body frame
    """
    rotm = Quat2Rotm(quat)
    dcm = rotm.T
    return dcm


def QuatMod(quat):
    """
    Calculates the module (Euclidean norm) of the input quaternion

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    quatMod : The module of the quaternion

    """
    quat = quat.reshape((4,))
    mod = np.linalg.norm(quat)
    return mod
    

def QuatConj(quat):
    """
    Calculates the quaternion conjugate

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    QuatConj : quaternion conjugate in the Hamilton form - [cos, isin, jsin, ksin]

    """
    quat = quat.reshape((4,))
    
    vectorPart = quat[1:]
    scalarPart = quat[0]
    
    quatConj = np.hstack((scalarPart, -vectorPart))
    return quatConj


def QuatNormalize(quat):
    """
    Normalizes the quaternion in input, dividing its components by its module

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    quatNormalized : the normalized quaternion in input in the Hamilton form - [cos, isin, jsin, ksin]

    """
    quat = quat.reshape((4,))

    mod = QuatMod(quat)
    
    quatNormalized = quat / mod
    return quatNormalized


def QuatInv(quat):
    """
    Calculates the quaternion inverse

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    quatInv: quaternion inverse in the Hamilton form - [cos, isin, jsin, ksin]

    """
    quat = quat.reshape((4,))
    
    mod = QuatMod(quat)
    conj = QuatConj(quat)
    
    quatInv = conj / (mod**2)
    return quatInv


def QuatMultiply(quat1, quat2):
    """
    Calculates the Hamilton product of two quaternions.\n
    WARNING: The operation is not commutative\n

    Parameters
    ----------
    quat1 : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n
    quat2 : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n

    Returns
    -------
    quat3 : the quaternion product of two input quaternions

    """
    quat1 = quat1.reshape((4,))
    quat2 = quat2.reshape((4,))
    
    v1 = quat1[1:]
    s1 = quat1[0]
    
    v2 = quat2[1:]
    s2 = quat2[0]

    scalarTerm = s1*s2 - v1 @ v2    
    vectorTerm = s2*v1 + s1*v2 + np.cross(v1, v2)    
    
    quat3 = np.hstack((scalarTerm, vectorTerm))
    return quat3
    
    
def QuatSum(quat1, quat2):
    """
    Calculates the sum of two quaternions

    Parameters
    ----------
    quat1 : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n
    quat2 : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n

    Returns
    -------
    quat3 : the quaternion sum of two input quaternions

    """
    quat1 = quat1.reshape((4,))
    quat2 = quat2.reshape((4,))
    
    v1 = quat1[1:]
    s1 = quat1[0]
    
    v2 = quat2[1:]
    s2 = quat2[0]
    
    scalare = s2 + s1
    vettoriale = v2 + v1
    quat3 = np.hstack((scalare, vettoriale))
    return quat3
    
  
def QuatRotate(vec, quat):
    
    """
    Rotates a 3D vector about a quaternion

    Parameters
    ----------
    vec : np.array (3,)\n
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n

    Returns
    -------
    vecPost : np.array (3,)

    """
    vecPre = Vec2Quat(vec)
    quat = quat.reshape((4,))
    q = QuatNormalize(quat)
    qi = QuatInv(q)
    
    prodotto = QuatMultiply(q, vecPre)
    vecPost = QuatMultiply(prodotto, qi)
    vecPost = vecPost[1:]
    return vecPost


def RotationAxisAngle2Quat(vers, teta):
    """
    Defines the quaternion corresponding to the rotation axis and rotation angle in input

    Parameters
    ----------
    vers : The rotation axis np.array(3,)\n
    teta : The rotation angle in degrees\n

    Returns
    -------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    """
    teta = np.radians(teta)
    vers = vers / np.linalg.norm(vers)
    
    C = np.cos(teta/2)
    S = np.sin(teta/2)
    
    quat = np.array([C, S*vers[0], S*vers[1], S*vers[2]]).astype(float)
    return quat


def Quat2RotationAngle(quat):
    """
    Extracts the rotation angle from the quaternion

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    teta : The rotation angle in degrees

    """
    quat = quat.reshape(4,)
    teta = np.degrees(2*np.arccos(quat[0]))
    return teta


def Quat2RotationAxis(quat):
    """
    Extracts the rotation axis from the quaternion

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]\n

    Returns
    -------
    vers : The rotation axis (versor) np.array(3,)

    """
    quat = quat.reshape(4,)
    teta = np.radians(Quat2RotationAngle(quat))
    S = np.sin(teta/2)
    
    vers = quat[1:] / S
    return vers


def Euler2Quat(roll, pitch, yaw):
    """
    Converts the Euler angles into the corresponding quaternion according to the aerospace sequence XYZ (or 321)

    Parameters
    ----------
    roll : The roll angle in degrees\n
    pitch : The pitch angle in degrees\n
    yaw : The yaw angle in degrees\n

    Returns
    -------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    """
    qR = RotationAxisAngle2Quat(VersorX, roll)
    qP = RotationAxisAngle2Quat(VersorY, pitch)
    qY = RotationAxisAngle2Quat(VersorZ, yaw)

    q1 = QuatMultiply(qP, qR)
    quat = QuatMultiply(qY, q1)

    return quat


def Rotm2Quat(rotm):
    """
    Converts a rotation matrix (in the body to earth frame formulation) into a quaternion

    Parameters
    ----------
    rotm : The rotation matrix np.array (3,3) 

    Returns
    -------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    """
    qw = 0.5*np.sqrt((1 + rotm[0,0] + rotm[1,1] + rotm[2,2]))
    
    qx = 0.5 * np.sign(rotm[2,1] - rotm[1,2]) * np.sqrt(rotm[0,0] - rotm[1,1] - rotm[2,2] + 1)
    
    qy = 0.5 * np.sign(rotm[0,2] - rotm[2,0]) * np.sqrt(rotm[1,1] - rotm[2,2] - rotm[0,0] + 1)
    
    qz = 0.5 * np.sign(rotm[1,0] - rotm[0,1]) * np.sqrt(rotm[2,2] - rotm[0,0] - rotm[1,1] + 1)
    
    quat = np.column_stack((qw,qx,qy,qz))
    quat = quat.reshape((4,))
    
    return quat


def Rotm2RotationAngle(rotm):
    """
    Extracts from the rotation matrix (in the body to earth frame formulation) the rotation angle for an axis-angle representation

    Parameters
    ----------
    rotm : The rotation matrix np.array(3,3)

    Returns
    -------
    teta : The rotation angle in degrees

    """
    teta = np.degrees(np.arccos((np.trace(rotm)-1)/2))
    return teta


def Rotm2RotationAxis(rotm):
    """
    Extracts from the rotation matrix (in the body to earth frame formulation) the rotation axis for an axis-angle representation

    Parameters
    ----------
    rotm : The rotation matrix np.array(3,3)

    Returns
    -------
    u : The rotation axis (versor) np.array(3,)

    """
    teta = Rotm2RotationAngle(rotm)
    u = np.array([rotm[2,1]-rotm[1,2], rotm[0,2]-rotm[2,0], rotm[1,0]-rotm[0,1]]).astype(float)

    if teta != 0.0:
        u = u / (2*np.sin(np.radians(teta)))

    return u


def RotationAxisAngle2Rotm(vers, teta):
    """
    Defines the rotation matrix corresponding to the rotation axis and rotation angle in input

    Parameters
    ----------
    vers : The rotation axis np.array(3,)\n
    teta : The rotation angle in degrees\n

    Returns
    -------
    rotm : The rotation matrix (in the body to earth frame formulation) np.array(3,)

    """
    teta = np.radians(teta)
    vers = vers / np.linalg.norm(vers)
    
    skewMat = Vec2SkewSymmetricMatrix(vers)
    
    rotm = np.cos(teta) * np.eye(3) + np.sin(teta) * skewMat + (1 - np.cos(teta)) * np.outer(vers, vers)
    
    return rotm


def Rotm2Euler(rotm):
    """
    Extracts the Euler angles from the rotation matrix according to the aerospace sequence ZYX (or 321)

    Parameters
    ----------
    rotm : The rotation matrix (from body to Earth frame formulation) np.array(3,)

    Returns
    -------
    roll : The roll angle in degrees\n
    pitch : The pitch angle in degrees\n
    yaw : The yaw angle in degrees\n

    """
    roll = np.arctan2(rotm[2,1], rotm[2,2])
    pitch = np.arctan2(-rotm[2,0], np.sqrt(rotm[2,1]**2 + rotm[2,2]**2))
    yaw = np.arctan2(rotm[1,0], rotm[0,0])
    
    roll = np.degrees(roll)
    pitch = np.degrees(pitch)
    yaw = np.degrees(yaw)
    
    return roll, pitch, yaw


def Euler2Rotm(roll, pitch, yaw):
    """
    Converts the Euler angles into a rotation matrix according to the aerospace sequence ZYX (or 321)

    Parameters
    ----------
    roll : The roll angle in degrees\n
    pitch : The pitch angle in degrees\n
    yaw : The yaw angle in degrees\n

    Returns
    -------
    rotm : The rotation matrix (from body to Earth frame formulation) np.array(3,3)

    """
    roll = np.radians(roll)
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    
    cosR = np.cos(roll)
    cosP = np.cos(pitch)
    cosY = np.cos(yaw)
    
    sinR = np.sin(roll)
    sinP = np.sin(pitch)
    sinY = np.sin(yaw)
    
    row1 = np.array([cosY*cosP, sinP*sinR*cosY - sinY*cosR, cosY*sinP*cosR + sinY*sinR]).astype(float)
    
    row2 = np.array([sinY*cosP, sinP*sinR*sinY + cosY*cosR, sinY*sinP*cosR - cosY*sinR]).astype(float)
    
    row3 = np.array([-sinP, sinR*cosP, cosR*cosP]).astype(float)
    
    rotm = np.row_stack((row1, row2, row3))
    
    return rotm


def Quat2Euler(quat):
    """
    Converts the quaternion into the corresponding Euler angles according to the aerospace sequence XYZ (or 321)

    Parameters
    ----------
    quat : quaternion in the Hamilton form - [cos, isin, jsin, ksin]

    Returns
    -------
    roll : The roll angle in degrees\n
    pitch : The pitch angle in degrees\n
    yaw : The yaw angle in degrees\n

    """
    quat = quat.reshape(4,)
    roll  = np.arctan2( 2*(quat[0]*quat[1] + quat[2]*quat[3]), 1 - 2*(quat[1]**2 + quat[2]**2) )
    pitch = np.arcsin ( 2*(quat[0]*quat[2] - quat[3]*quat[1]) )
    yaw   = np.arctan2( 2*(quat[0]*quat[3] + quat[1]*quat[2]), 1 - 2*(quat[2]**2 + quat[3]**2) )
    
    roll = np.degrees(roll)
    pitch = np.degrees(pitch)
    yaw = np.degrees(yaw)
    
    return roll, pitch, yaw
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
