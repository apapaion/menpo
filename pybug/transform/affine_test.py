import numpy as np
from numpy.testing import assert_allclose, assert_equal
from pybug.transform.affine import Rotation, Translation
from pybug.exceptions import DimensionalityError
from nose.tools import raises
from pybug.transform.affine import AffineTransform, SimilarityTransform

@raises(DimensionalityError)
def test_1d():
    t_vec = np.array([1])
    Translation(t_vec)


@raises(DimensionalityError)
def test_5d():
    t_vec = np.ones(5)
    Translation(t_vec)


def test_translation():
    t_vec = np.array([1, 2, 3])
    starting_vector = np.random.rand(10, 3)
    transform = Translation(t_vec)
    transformed = transform.apply(starting_vector)
    assert_allclose(starting_vector + t_vec, transformed)


def test_basic_2d_rotation():
    rotation_matrix = np.array([[0, 1],
                                [-1, 0]])
    rotation = Rotation(rotation_matrix)
    assert_allclose(np.array([0, -1]), rotation.apply(np.array([1, 0])))


def test_basic_2d_rotation_axis_angle():
    rotation_matrix = np.array([[0, 1],
                                [-1, 0]])
    rotation = Rotation(rotation_matrix)
    axis, angle = rotation.axis_and_angle_of_rotation()
    assert_allclose(axis, np.array([0, 0, 1]))
    assert_allclose((90 * np.pi)/180, angle)


def test_basic_3d_rotation():
    a = np.sqrt(3.0)/2.0
    b = 0.5
    # this is a rotation of -30 degrees about the x axis
    rotation_matrix = np.array([[1, 0, 0],
                                [0, a, b],
                                [0, -b, a]])
    rotation = Rotation(rotation_matrix)
    starting_vector = np.array([0, 1, 0])
    transformed = rotation.apply(starting_vector)
    assert_allclose(np.array([0, a, -b]), transformed)


def test_basic_3d_rotation_axis_angle():
    a = np.sqrt(3.0)/2.0
    b = 0.5
    # this is a rotation of -30 degrees about the x axis
    rotation_matrix = np.array([[1, 0, 0],
                                [0, a, b],
                                [0, -b, a]])
    rotation = Rotation(rotation_matrix)
    axis, angle = rotation.axis_and_angle_of_rotation()
    assert_allclose(axis, np.array([1, 0, 0]))
    assert_allclose((-30 * np.pi)/180, angle)


def test_3d_rotation_inverse_eye():
    a = np.sqrt(3.0)/2.0
    b = 0.5
    # this is a rotation of -30 degrees about the x axis
    rotation_matrix = np.array([[1, 0, 0],
                                [0, a, b],
                                [0, -b, a]])
    rotation = Rotation(rotation_matrix)
    transformed = rotation.compose(rotation.inverse)
    print transformed.homogeneous_matrix
    assert_allclose(np.eye(4), transformed.homogeneous_matrix, atol=1e-15)

jac_solution2d = np.array(
    [[[0.,  0.],
    [0.,  0.],
    [0.,  0.],
    [0.,  0.],
    [1.,  0.],
    [0.,  1.]],
    [[0.,  0.],
    [0.,  0.],
    [1.,  0.],
    [0.,  1.],
    [1.,  0.],
    [0.,  1.]],
    [[0.,  0.],
    [0.,  0.],
    [2.,  0.],
    [0.,  2.],
    [1.,  0.],
    [0.,  1.]],
    [[1.,  0.],
    [0.,  1.],
    [0.,  0.],
    [0.,  0.],
    [1.,  0.],
    [0.,  1.]],
    [[1.,  0.],
    [0.,  1.],
    [1.,  0.],
    [0.,  1.],
    [1.,  0.],
    [0.,  1.]],
    [[1.,  0.],
    [0.,  1.],
    [2.,  0.],
    [0.,  2.],
    [1.,  0.],
    [0.,  1.]]])

jac_solution3d = np.array(
    [[[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [2.,  0.,  0.],
    [0.,  2.,  0.],
    [0.,  0.,  2.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [2.,  0.,  0.],
    [0.,  2.,  0.],
    [0.,  0.,  2.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [2.,  0.,  0.],
    [0.,  2.,  0.],
    [0.,  0.,  2.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [0.,  0.,  0.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]],
    [[1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [2.,  0.,  0.],
    [0.,  2.,  0.],
    [0.,  0.,  2.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.],
    [1.,  0.,  0.],
    [0.,  1.,  0.],
    [0.,  0.,  1.]]])


def test_affine_jacobian_2d_with_positions():
    params = np.array([0, 0.1, 0.2, 0, 30, 70])
    t = AffineTransform.from_vector(params)
    explicit_pixel_locations = np.array(
        [[0, 0],
        [0, 1],
        [0, 2],
        [1, 0],
        [1, 1],
        [1, 2]])
    dW_dp = t.jacobian(explicit_pixel_locations)
    assert_equal(dW_dp, jac_solution2d)


def test_affine_jacobian_3d_with_positions():
    params = np.ones(12)
    t = AffineTransform.from_vector(params)
    explicit_pixel_locations = np.array(
        [[0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [0, 2, 0],
        [0, 2, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
        [1, 2, 0],
        [1, 2, 1]])
    dW_dp = t.jacobian(explicit_pixel_locations)
    assert_equal(dW_dp, jac_solution3d)


def test_similarity_2d_from_vector():
    params = np.array([0.2, 0.1, 1, 2])
    homo = np.array([[params[0] + 1, -params[1], params[2]],
                     [params[1], params[0] + 1, params[3]],
                     [0, 0, 1]])

    sim = SimilarityTransform.from_vector(params)

    assert_equal(sim.homogeneous_matrix, homo)


def test_similarity_2d_as_vector():
    params = np.array([0.2, 0.1, 1.0, 2.0])
    homo = np.array([[params[0] + 1.0, -params[1], params[2]],
                     [params[1], params[0] + 1.0, params[3]],
                     [0.0, 0.0, 1.0]])

    vec = SimilarityTransform(homo).as_vector()

    assert_allclose(vec, params)


def test_translation_2d_from_vector():
    params = np.array([1, 2])
    homo = np.array([[1, 0, params[0]],
                     [0, 1, params[1]],
                     [0, 0, 1]])

    tr = Translation.from_vector(params)

    assert_equal(tr.homogeneous_matrix, homo)


def test_translation_2d_as_vector():
    params = np.array([1, 2])

    vec = Translation(params).as_vector()

    assert_allclose(vec, params)


def test_translation_3d_from_vector():
    params = np.array([1, 2, 3])
    homo = np.array([[1, 0, 0, params[0]],
                     [0, 1, 0, params[1]],
                     [0, 0, 1, params[2]],
                     [0, 0, 0, 1]])

    tr = Translation.from_vector(params)

    assert_equal(tr.homogeneous_matrix, homo)


def test_translation_3d_as_vector():
    params = np.array([1, 2, 3])

    vec = Translation(params).as_vector()

    assert_allclose(vec, params)