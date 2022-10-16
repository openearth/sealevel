#!/usr/bin/env python3

import pandas as pd
import numpy as np

import pytest

import slr.models


@pytest.fixture
def df_linear():
    """create a dataframe where sea level is 0.1 * year since 1900"""
    rows = []
    for year in range(1900, 2020):
        row = {"year": year, "height": (year - 1970) * 0.1}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


@pytest.fixture
def df_quadratic():
    """create a dataframe where sea level is 0.1 * year since 1900"""
    rows = []
    epoch = 1970
    for year in range(1900, 2020):
        height = 0.1 * (year - 1970) * 0.1 + 0.2 * (year - epoch) ** 2
        row = {"year": year, "height": height}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


@pytest.fixture
def df_nodal():
    """create a dataframe where sea level is 0.1 * year since 1900"""
    rows = []
    epoch = 1970
    for year in range(1900, 2020):
        height = 0.1 * (year - epoch) * 0.1 + 0.2 * (year - epoch) ** 2
        height += 0.3 * np.sin(2 * np.pi * (year - epoch) / 18.613)
        row = {"year": year, "height": height}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


@pytest.fixture
def df_acceleration_1960():
    """create a dataframe where sea level is 0.1 * year since 1900"""
    rows = []
    epoch = 1970
    for year in range(1900, 2020):
        height = 0.1 * (year - epoch)
        if year >= 1960:
            height += 0.5 * (year - 1960) * (year - 1960)
        row = {"year": year, "height": height}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def test_quadratic_model_linear_data(df_linear):
    """test whether we get correct results with linear input"""
    fit, names = slr.models.quadratic_model(df_linear, with_wind=False, with_ar=False)

    np.testing.assert_almost_equal(fit.params["const"], 0, decimal=5)
    np.testing.assert_almost_equal(fit.params["x1"], 0.1, decimal=0.5)


def test_quadratic_model_quadratic_data(df_quadratic):
    """test whether we get correct results with quadratic input"""
    fit, names = slr.models.quadratic_model(
        df_quadratic, with_wind=False, with_ar=False
    )

    np.testing.assert_almost_equal(fit.params["const"], 0, decimal=5)
    np.testing.assert_almost_equal(fit.params["x1"], 0.1, decimal=0.5)
    np.testing.assert_almost_equal(fit.params["x2"], 0.2, decimal=0.5)
    np.testing.assert_almost_equal(fit.params["x3"], 0, decimal=0.5)


def test_quadratic_model_nodal_data(df_nodal):
    """test whether we get correct results with quadratic input"""
    fit, names = slr.models.quadratic_model(df_nodal, with_wind=False, with_ar=False)
    print(fit.params)

    np.testing.assert_almost_equal(fit.params["const"], 0, decimal=5)
    np.testing.assert_almost_equal(fit.params["x1"], 0.1, decimal=0.5)
    np.testing.assert_almost_equal(fit.params["x2"], 0.2, decimal=0.5)
    np.testing.assert_almost_equal(fit.params["x4"], 0.3, decimal=0.5)


def test_quadratic_model_acceleration_1960_data(df_acceleration_1960):
    """test whether we get correct results with quadratic input"""
    fit, names = slr.models.quadratic_model(
        df_acceleration_1960,
        with_wind=False,
        with_ar=False,
        start_acc=1960,
    )

    # constant now refers to 1960
    np.testing.assert_almost_equal(fit.params["const"], -1, decimal=5)
    np.testing.assert_almost_equal(fit.params["x1"], 0.1, decimal=0.5)
    np.testing.assert_almost_equal(fit.params["x2"], 0.5, decimal=0.5)
