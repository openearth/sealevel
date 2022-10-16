import numpy as np
import statsmodels.api as sm

# define the statistical model
def linear_acceleration_model(df):
    """define a simple linear model, with nodal tide and without wind (no acceleration)"""
    y = df["height"]
    X = np.c_[
        df["year"] - 1970,
        (df["year"] - 1970) * (df["year"] - 1970),
        np.cos(2 * np.pi * (df["year"] - 1970) / 18.613),
        np.sin(2 * np.pi * (df["year"] - 1970) / 18.613),
    ]
    month = np.mod(df["year"], 1) * 12.0
    names = ["Constant", "Trend", "Acceleration", "Nodal U", "Nodal V"]
    X = sm.add_constant(X)
    model = sm.OLS(y, X, missing="drop")
    fit = model.fit()
    return fit, names


# define the statistical model
def quadratic_model(df, with_wind=True, with_ar=True, with_nodal=True, start_acc=None):
    """This model computes a parabolic linear fit. This corresponds to the hypothesis that sea-level is accelerating."""

    y = df["height"]

    epoch = 1970
    if start_acc:
        epoch = start_acc

    # linear term, 0 in 1970, 30 in 2000
    linear_term = df["year"] - epoch

    # use quadratic term since epoch for comparison with other models.
    # 1 in 1969, 0 in 1970, 1 in 1971, 4 in 1972, masked if before start_acc
    quadratic_term = (df["year"] - epoch) * (df["year"] - epoch)
    if start_acc is not None:
        quadratic_term = (df["year"] >= start_acc) * (df["year"] - epoch) ** 2

    # regression terms
    X = np.c_[linear_term, quadratic_term]
    names = [
        "Constant (in year {epoch})",
        "Trend",
        f"Acceleration from {start_acc}",
    ]

    if with_nodal:
        nodal_cos_term = np.cos(2 * np.pi * (df["year"] - epoch) / 18.613)
        nodal_sin_term = np.sin(2 * np.pi * (df["year"] - epoch) / 18.613)
        X = np.c_[X, nodal_cos_term, nodal_sin_term]
        names.extend(["Nodal U", "Nodal V"])

    if with_wind:
        X = np.c_[X, df["u2"], df["v2"]]
        names.extend(["Wind $u^2$", "Wind $v^2$"])

    # add constant to the start
    X = sm.add_constant(X)

    if with_ar:
        model = sm.GLSAR(y, X, missing="drop", rho=1)
        fit = model.iterative_fit(cov_type="HC0")
    else:
        model = sm.OLS(y, X, missing="drop")
        fit = model.fit(cov_type="HC0")

    return fit, names


# define the statistical model
def broken_linear_model(df, with_wind=True):
    """This model fits the sea-level rise has started to rise faster in 1993."""
    y = df["height"]
    X = np.c_[
        df["year"] - 1970,
        (df["year"] > 1993) * (df["year"] - 1993),
        np.cos(2 * np.pi * (df["year"] - 1970) / 18.613),
        np.sin(2 * np.pi * (df["year"] - 1970) / 18.613),
    ]
    names = ["Constant", "Trend", "+trend (1993)", "Nodal U", "Nodal V"]
    if with_wind:
        X = np.c_[X, df["u2"], df["v2"]]
        names.extend(["Wind $u^2$", "Wind $v^2$"])
    X = sm.add_constant(X)
    model_broken_linear = sm.GLSAR(y, X, rho=1)
    fit = model_broken_linear.iterative_fit(cov_type="HC0")
    return fit, names


def linear_model(df, with_wind=True, with_ar=True):
    """Define the linear model with optional wind and autoregression.
    See the latest report for a detailed description.
    """

    y = df["height"]
    X = np.c_[
        df["year"] - 1970,
        np.cos(2 * np.pi * (df["year"] - 1970) / 18.613),
        np.sin(2 * np.pi * (df["year"] - 1970) / 18.613),
    ]
    month = np.mod(df["year"], 1) * 12.0
    names = ["Constant", "Trend", "Nodal U", "Nodal V"]
    if with_wind:
        X = np.c_[X, df["u2"], df["v2"]]
        names.extend(["Wind $u^2$", "Wind $v^2$"])
    X = sm.add_constant(X)
    if with_ar:
        model = sm.GLSAR(y, X, missing="drop", rho=1)
    else:
        model = sm.OLS(y, X, missing="drop")
    fit = model.fit(cov_type="HC0")
    return fit, names
