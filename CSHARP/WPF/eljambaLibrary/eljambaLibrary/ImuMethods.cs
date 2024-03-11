using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Media3D;


namespace eljambaLibrary
{
    public class ImuMethods
    {
        //MAI USATA!! INUTILE PERCHE' C'E' MATRIX3D
        public class RotationMatrix
        {
            public double[][][] element;

            /// <summary>
            /// Structure builder of a 3 x 3 x 'samplesNumber' double matrix
            /// </summary>
            /// <remarks>
            /// 'element' is a double jagged array
            /// RotationMatrixelement.Length = 3, number of rows
            /// RotationMatrixelement[0].Length = 3, number of columns
            /// RotationMatrixelement[0][0].Length = samplesNumber, number of samples
            /// </remarks>
            public RotationMatrix(int samplesNumber)
            {
                element = new double[3][][];
                for (var i = 0; i < element.Length; i++)
                {
                    element[i] = new double[3][];
                    for (var j = 0; j < element[i].Length; j++)
                    {
                        element[i][j] = new double[samplesNumber];
                    }
                }
            }
        }


        //MAI USATA!!
        public class QuaternionWXYZ
        {
            public double[] w, x, y, z;

            /// <summary>
            /// Structure builder of 4 double arrays (w,x,y,z) 'samplesNumber' length
            /// </summary>
            /// <remarks>
            /// QuaternionWXYZ.w.Length == QuaternionWXYZ.x.Length == QuaternionWXYZ.y.Length == QuaternionWXYZ.z.Length == samplesNumber
            /// </remarks>
            public QuaternionWXYZ(int samplesNumber)
            {
                w = new double[samplesNumber];
                x = new double[samplesNumber];
                y = new double[samplesNumber];
                z = new double[samplesNumber];

            }
        }


        //MAI USATA!!
        public class QuaternionJagged
        {
            public double[][] elem;

            /// <summary>
            /// Structure builder of a 4 x 'samplesNumber' double array
            /// </summary>
            /// <remarks>
            /// QuaternionJagged.elem.Length == 4, number of arrays 
            /// 0 -> w component  ||  1 -> x component  ||  2 -> y component  ||  3 -> z component
            /// QuaternionJagged.elem[0].Length == QuaternionJagged.elem[1].Length == QuaternionJagged.elem[2].Length == QuaternionJagged.elem[3].Length == 'samplesNumber'
            /// </remarks>
            public QuaternionJagged(int samplesNumber)
            {
                elem = new double[4][];
                for(var i = 0; i < elem.Length; i++)
                {
                    elem[i] = new double[samplesNumber];
                }
            }

        }


        public class myQuaternion
        {
            public double w, x, y, z;

            /// <summary>
            /// Structures builder
            /// </summary>
            public myQuaternion()
            {
                w = new double();
                x = new double();
                y = new double();
                z = new double();

            }
        }




        /// <summary>
        /// MAI USATO!!!! This method calculates the matrix product NOT COMMUTATIVE between two matrix
        /// </summary>
        public RotationMatrix MatrixProduct(RotationMatrix A, RotationMatrix B)
        {
            RotationMatrix product = new RotationMatrix(A.element[0][0].Length);

            for (var sample = 0; sample < product.element[0][0].Length; sample++)
            {
                for (var row = 0; row < product.element.Length; row++)
                {
                    for (var col = 0; col < product.element[0].Length; col++)
                    {
                        product.element[row][col][sample] = 0.0f;
                        for (var k = 0; k < A.element[0].Length; k++)  //OR k < B.element.length;
                        {
                            product.element[row][col][sample] = product.element[row][col][sample] + (A.element[row][k][sample] * B.element[k][col][sample]);
                        }
                    }
                }
            }

            return product;

        }



        /// <summary>
        /// MAI USATO!!!! This method converts a quaternion (QuaternionWXYZ) into a rotation matrix
        /// </summary>
        public RotationMatrix FromQuaternionToRotationMatrix(QuaternionWXYZ quat)
        {
            RotationMatrix matrix = new RotationMatrix(quat.w.Length);

            //ciclo sui campioni
            for(var sample = 0; sample < quat.w.Length; sample++)
            {
                //prima colonna
                matrix.element[0][0][sample] = 1 - 2 * (Math.Pow(quat.y[sample],2) + Math.Pow(quat.z[sample],2));
                matrix.element[1][0][sample] = 2 * (quat.x[sample] * quat.y[sample] - quat.w[sample] * quat.z[sample]);
                matrix.element[2][0][sample] = 2 * (quat.x[sample] * quat.z[sample] + quat.w[sample] * quat.y[sample]);

                //seconda colonna
                matrix.element[0][1][sample] = 2 * (quat.x[sample] * quat.y[sample] + quat.w[sample] * quat.z[sample]);
                matrix.element[1][1][sample] = 1 - 2 * (Math.Pow(quat.x[sample], 2) + Math.Pow(quat.z[sample], 2));
                matrix.element[2][1][sample] = 2 * (quat.y[sample] * quat.z[sample] - quat.w[sample] * quat.x[sample]);

                //terza colonna
                matrix.element[0][2][sample] = 2 * (quat.x[sample] * quat.z[sample] - quat.w[sample] * quat.y[sample]);
                matrix.element[1][2][sample] = 2 * (quat.y[sample] * quat.z[sample] + quat.w[sample] * quat.x[sample]);
                matrix.element[2][2][sample] = 1 - 2 * (Math.Pow(quat.x[sample], 2) + Math.Pow(quat.y[sample], 2));

            }

            return matrix;
        }



        /// <summary>
        /// MAI USATO!!!! This method converts a quaternion (QuaternionJagged) into a rotation matrix
        /// </summary>
        public RotationMatrix FromQuaternionToRotationMatrix(QuaternionJagged quat)
        {
            RotationMatrix matrix = new RotationMatrix(quat.elem[0].Length);

            //ciclo sui campioni
            for (var sample = 0; sample < quat.elem[0].Length; sample++)
            {
                //prima colonna
                matrix.element[0][0][sample] = 1 - 2 * (Math.Pow(quat.elem[2][sample], 2) + Math.Pow(quat.elem[3][sample], 2));
                matrix.element[1][0][sample] = 2 * (quat.elem[1][sample] * quat.elem[2][sample] - quat.elem[0][sample] * quat.elem[3][sample]);
                matrix.element[2][0][sample] = 2 * (quat.elem[1][sample] * quat.elem[3][sample] + quat.elem[0][sample] * quat.elem[2][sample]);

                //seconda colonna
                matrix.element[0][1][sample] = 2 * (quat.elem[1][sample] * quat.elem[2][sample] + quat.elem[0][sample] * quat.elem[3][sample]);
                matrix.element[1][1][sample] = 1 - 2 * (Math.Pow(quat.elem[1][sample], 2) + Math.Pow(quat.elem[3][sample], 2));
                matrix.element[2][1][sample] = 2 * (quat.elem[2][sample] * quat.elem[3][sample] - quat.elem[0][sample] * quat.elem[1][sample]);

                //terza colonna
                matrix.element[0][2][sample] = 2 * (quat.elem[1][sample] * quat.elem[3][sample] - quat.elem[0][sample] * quat.elem[2][sample]);
                matrix.element[1][2][sample] = 2 * (quat.elem[2][sample] * quat.elem[3][sample] + quat.elem[0][sample] * quat.elem[1][sample]);
                matrix.element[2][2][sample] = 1 - 2 * (Math.Pow(quat.elem[1][sample], 2) + Math.Pow(quat.elem[2][sample], 2));

            }

            return matrix;
        }



        /// <summary>
        /// MAI USATO!!!! This method corrects Cometa Imu Rotation Matrix
        /// </summary>
        public RotationMatrix CorrectCometaRotationMatrix(RotationMatrix matrix)
        {
            RotationMatrix temp = new RotationMatrix(matrix.element[0][0].Length);



            return temp;
        }



        /// <summary>
        /// Returns the Hamiltonian product (not commutative) between two quaternions;
        /// </summary>
        public myQuaternion QuatMultiply(myQuaternion a, myQuaternion b)
        {
            myQuaternion prod = new myQuaternion();

            prod.w = (a.w * b.w) - (a.x * b.x) - (a.y * b.y) - (a.z * b.z);
            prod.x = (a.x * b.w) + (a.w * b.x) - (a.z * b.y) + (a.y * b.z);
            prod.y = (a.y * b.w) + (a.z * b.x) + (a.w * b.y) - (a.x * b.z);
            prod.z = (a.z * b.w) - (a.y * b.x) + (a.x * b.y) + (a.w * b.z);

            return prod;
        }



        /// <summary>
        /// Returns the flexion, adduction, and rotationi angles.
        /// The two reference frames MUST have X axis pointing in the direction of motion (adduction axis), 
        /// Y pointing upward (rotation axis) and Z rightward (flexion axis).
        ///        
        /// output.X -> flexion   angle
        /// output.Y -> adduction angle
        /// output.Z -> rotation  angle
        /// </summary>
        public Vector3D CalcAngoli(Vector3D ProxY, Vector3D ProxZ, Vector3D DistY, Vector3D DistZ)
        {
            Vector3D nodi = new Vector3D();
            Vector3D angoli = new Vector3D();

                nodi = Vector3D.CrossProduct(DistY, ProxZ);
                nodi.Normalize();
                //adduction angle
                angoli.Y = 0.5 * Math.PI - Math.Acos(Vector3D.DotProduct(ProxZ, DistY));
                //rotation angle
                angoli.Z = 0.5 * Math.PI - Math.Acos(Vector3D.DotProduct(nodi, DistZ));

                if (Vector3D.DotProduct(Vector3D.CrossProduct(nodi, ProxY), ProxZ) > 0)
                {
                    //flexion angle
                    angoli.X = 0.5 * Math.PI - Math.Acos(Vector3D.DotProduct(nodi, ProxY));
                }
                else
                {
                    //flexion angle
                    angoli.X = 0.5 * Math.PI - (2 * Math.PI - Math.Acos(Vector3D.DotProduct(nodi, ProxY)));
                }
            
            return angoli;

        }



        /// <summary>
        /// Returns the rotation matrix equivalent to the input quaternion.
        /// </summary>
        public Matrix3D Quat2Rotm(myQuaternion myQuat)
        {
            Matrix3D mat = new Matrix3D();

            mat.M11 = 1 - 2 * (Math.Pow(myQuat.y, 2) + Math.Pow(myQuat.z, 2));
            mat.M12 = 2 * (myQuat.x * myQuat.y - myQuat.w * myQuat.z);
            mat.M13 = 2 * (myQuat.x * myQuat.z - myQuat.w * myQuat.y);

            mat.M21 = 2 * (myQuat.x * myQuat.y - myQuat.w * myQuat.z);
            mat.M22 = 1 - 2 * (Math.Pow(myQuat.x, 2) + Math.Pow(myQuat.z, 2));
            mat.M23 = 2 * (myQuat.y * myQuat.z - myQuat.w * myQuat.x);

            mat.M31 = 2 * (myQuat.x * myQuat.z - myQuat.w * myQuat.y);
            mat.M32 = 2 * (myQuat.y * myQuat.z + myQuat.w * myQuat.x);
            mat.M33 = 1 - 2 * (Math.Pow(myQuat.x, 2) + Math.Pow(myQuat.y, 2));            

            return mat;

        }



        /// <summary>
        /// This method calculates the absolute reference system rearranging the pelvis one.
        /// Xabs = -Zpelvis; Yabs = -Xpelvis; Zabs = Ypelvis;
        /// </summary>
        public Matrix3D DefineAbsoluteReferenceSystem(myQuaternion pelvisQuat)
        {
            Matrix3D temp = Quat2Rotm(pelvisQuat); //temp contiene comunque solo un campione
            Matrix3D myAbs = new Matrix3D();

            //X = -Zpelvis
            myAbs.M11 = -temp.M13;
            myAbs.M21 = -temp.M23;
            myAbs.M31 = -temp.M33;

            //Y = -Xpelvis
            myAbs.M12 = -temp.M11;
            myAbs.M22 = -temp.M21;
            myAbs.M32 = -temp.M31;

            //Z = Ypelvis
            myAbs.M13 = temp.M12;
            myAbs.M23 = temp.M22;
            myAbs.M33 = temp.M32;

            return myAbs;

        }

        

        /// <summary>
        /// Returns the rotated quaternion of the input one.
        /// +90° (anti-clockwise) rotation occurs around Z axis.
        /// X_new = Y_old; Y_new = - X_old
        /// </summary>
        public myQuaternion RotateCometaQuaternion(myQuaternion inputQuat)
        {
            myQuaternion correction = new myQuaternion();
            myQuaternion correctedQuat = new myQuaternion();

            //definisco il quaternione correzione
            correction.w = Math.Cos(0.25 * Math.PI);
            correction.x = 0;
            correction.y = 0;
            correction.z = Math.Sin(0.25 * Math.PI);

            correctedQuat = QuatMultiply(inputQuat, correction);

            return correctedQuat;

        }

        


    }
}
