from jpype import *
import random
import math

# Change location of jar to match yours:
jarLocation = "../../infodynamics.jar"
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Generate some random normalised data.
numObservations = 288  #1000
covariance=0.4
# Source array of random normals:
#sourceArray = [random.normalvariate(0,1) for r in range(numObservations)]
sourceArray = [15, 18, 8, 0, 6, 6, 6, 3, 5, 11, 6, 6, 6, 12, 9, 4, 7, 2, 5, 0, 9, 5, 4, 3, 3, 4, 4, 2, 0, 2, 2, 5, 0, 3, 4, 3, 0, 3, 4, 8, 3, 8, 5, 0, 2, 11, 2, 5, 6, 7, 7, 2, 6, 8, 4, 8, 11, 5, 18, 2, 38, 34, 14, 56, 30, 37, 34, 30, 52, 76, 68, 71, 79, 103, 84, 92, 105, 101, 134, 158, 266, 221, 190, 192, 322, 239, 224, 248, 203, 254, 215, 250, 260, 268, 281, 284, 228, 226, 171, 157, 182, 139, 203, 127, 143, 173, 112, 134, 137, 138, 136, 156, 127, 128, 198, 160, 110, 91, 116, 123, 123, 106, 103, 139, 148, 128, 110, 115, 65, 123, 174, 167, 128, 155, 177, 132, 184, 168, 246, 275, 209, 253, 221, 194, 179, 160, 217, 253, 245, 237, 268, 178, 142, 133, 164, 168, 126, 140, 186, 138, 174, 126, 151, 150, 209, 184, 141, 167, 166, 234, 208, 157, 143, 118, 152, 140, 156, 116, 137, 169, 194, 163, 185, 211, 185, 231, 229, 227, 208, 232, 179, 196, 194, 199, 220, 219, 263, 247, 210, 242, 289, 353, 336, 294, 291, 230, 235, 216, 222, 181, 226, 188, 233, 228, 179, 196, 199, 223, 188, 207, 162, 172, 134, 161, 135, 120, 155, 142, 154, 145, 142, 105, 151, 117, 114, 138, 108, 64, 100, 138, 113, 125, 122, 113, 98, 111, 89, 86, 110, 139, 121, 113, 95, 92, 94, 85, 89, 69, 103, 94, 108, 151, 76, 63, 77, 48, 69, 107, 66, 68, 93, 61, 94, 101, 25, 31, 40, 27, 57, 41, 42, 38, 8, 33, 27, 16, 11, 18]
# Destination array of random normals with partial correlation to previous value of sourceArray
destArray = [0] + [sum(pair) for pair in zip([covariance*y for y in sourceArray[0:numObservations-1]], \
                                             [(1-covariance)*y for y in [random.normalvariate(0,1) for r in range(numObservations-1)]] ) ]
# Uncorrelated source array:
destArray =[15, 17, 8, 6, 9, 5, 2, 13, 21, 6, 7, 2, 5, 9, 7, 5, 3, 3, 0, 2, 3, 3, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0, 3, 4, 6, 0, 0, 2, 5, 4, 2, 3, 2, 0, 0, 2, 0, 6, 3, 5, 4, 0, 9, 21, 8, 22, 22, 0, 13, 24, 13, 18, 24, 30, 28, 27, 36, 35, 23, 35, 51, 45, 93, 97, 62, 95, 88, 108, 52, 131, 165, 129, 182, 129, 219, 199, 169, 198, 224, 210, 201, 318, 425, 259, 297, 255, 251, 276, 211, 203, 176, 167, 182, 152, 184, 168, 161, 109, 152, 155, 162, 131, 176, 139, 314, 164, 181, 141, 110, 129, 150, 158, 175, 120, 166, 168, 159, 150, 249, 145, 174, 177, 170, 157, 164, 179, 130, 183, 190, 219, 209, 191, 232, 197, 163, 226, 196, 233, 231, 212, 248, 220, 222, 219, 172, 174, 145, 195, 177, 186, 126, 169, 187, 277, 215, 123, 146, 150, 169, 204, 222, 171, 165, 167, 165, 183, 150, 162, 202, 200, 178, 222, 198, 222, 173, 184, 190, 240, 182, 217, 235, 224, 228, 225, 252, 223, 293, 295, 230, 264, 344, 280, 300, 318, 256, 282, 258, 254, 249, 259, 236, 224, 307, 303, 168, 229, 182, 206, 241, 220, 185, 146, 165, 221, 158, 123, 185, 128, 159, 115, 129, 155, 139, 89, 124, 97, 69, 83, 96, 84, 153, 106, 78, 117, 71, 81, 79, 76, 82, 105, 61, 74, 79, 60, 55, 66, 69, 97, 84, 45, 81, 60, 84, 59, 64, 44, 73, 62, 71, 82, 45, 41, 55, 71, 37, 40, 55, 91, 57, 65, 27, 36, 26, 50, 12, 30, 17, 29]
sourceArray2 = [random.normalvariate(0,1) for r in range(numObservations)]
# Create a TE calculator and run it:
teCalcClass = JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
teCalc = teCalcClass()
teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units

teCalc.setObservations(JArray(JDouble, 1)(sourceArray), JArray(JDouble, 1)(destArray))
# For copied source, should give something close to 1 bit:
result = teCalc.computeAverageLocalOfObservations()
print("TE result %.4f bits; expected to be close to %.4f bits for these correlated Gaussians but biased upwards" % \
    (result, math.log(1/(1-math.pow(covariance,2)))/math.log(2)))

teCalc.initialise() # Initialise leaving the parameters the same
teCalc.setObservations(JArray(JDouble, 1)(destArray), JArray(JDouble, 1)(sourceArray))
result = teCalc.computeAverageLocalOfObservations()
print("TE result %.4f bits; expected to be close to %.4f bits for these correlated Gaussians but biased upwards" % \
    (result, math.log(1/(1-math.pow(covariance,2)))/math.log(2)))
