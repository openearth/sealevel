import numpy as np
import statsmodels.api as sm


def quadratic_model(
    df, with_wind=True, with_ar=True, with_nodal=True, quantity="height"
):
    """This model computes a parabolic linear fit. This corresponds to the hypothesis that sea-level is accelerating."""

    y = df[quantity]

    epoch = 1970

    # linear term, 0 in 1970, 30 in 2000
    linear_term = df["year"] - epoch

    # use quadratic term since epoch for comparison with other models.
    # 1 in 1969, 0 in 1970, 1 in 1971, 4 in 1972, masked if before start_acc
    quadratic_term = (df["year"] - epoch) * (df["year"] - epoch)

    # regression terms
    X = np.c_[linear_term, quadratic_term]
    names = [
        f"Constant (in year {epoch})",
        "Trend",
        "Acceleration",
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


def broken_quadratic_model(
    df,
    with_wind=True,
    with_ar=True,
    with_nodal=True,
    start_acceleration=1960,
    quantity="height",
):
    """This model computes a parabolic linear fit, starting in year start_accleration. This corresponds to the hypothesis that sea-level is accelerating since start_acceleration."""

    y = df[quantity]

    # linear term, 0 in 1970, 30 in 2000
    linear_term = df["year"] - start_acceleration

    # use quadratic term since epoch for comparison with other models.
    # 1 in 1969, 0 in 1970, 1 in 1971, 4 in 1972, masked if before start_acceleration
    quadratic_term = (df["year"] >= start_acceleration) * (
        df["year"] - start_acceleration
    ) ** 2

    # regression terms
    X = np.c_[linear_term, quadratic_term]
    names = [
        f"Constant (in year {start_acceleration})",
        "Trend",
        f"Acceleration from {start_acceleration}",
    ]

    if with_nodal:
        # always relative to 1970
        nodal_cos_term = np.cos(2 * np.pi * (df["year"] - 1970) / 18.613)
        nodal_sin_term = np.sin(2 * np.pi * (df["year"] - 1970) / 18.613)
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
def broken_linear_model(
    df, with_wind=True, with_ar=True, quantity="height", start_acceleration=1993
):
    """This model fits the sea-level rise has started to rise faster in epoch."""
    y = df[quantity]
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
    if with_ar:
        model = sm.GLSAR(y, X, missing="drop", rho=1)
        fit = model.iterative_fit(cov_type="HC0")

    else:
        model = sm.OLS(y, X, missing="drop")
        fit = model.fit(cov_type="HC0")

    return fit, names


def linear_model(df, with_wind=True, with_ar=True, quantity="height"):
    """Define the linear model with optional wind and autoregression.
    See the latest report for a detailed description.
    """

    y = df[quantity]
    X = np.c_[
        df["year"] - 1970,
        np.cos(2 * np.pi * (df["year"] - 1970) / 18.613),
        np.sin(2 * np.pi * (df["year"] - 1970) / 18.613),
    ]
    names = ["Constant", "Trend", "Nodal U", "Nodal V"]
    if with_wind:
        X = np.c_[X, df["u2"], df["v2"]]
        names.extend(["Wind $u^2$", "Wind $v^2$"])
    X = sm.add_constant(X)
    if with_ar:
        model = sm.GLSAR(y, X, missing="drop", rho=1)
        fit = model.iterative_fit(cov_type="HC0")
    else:
        model = sm.OLS(y, X, missing="drop")
        fit = model.fit(cov_type="HC0")
    return fit, names


def tide_effect(fit, names):

    # Nodal parameters should be stored as x2, x3 in the fit
    u_index = names.index('Nodal U')
    v_index = names.index('Nodal V')

    u_name = fit.model.exog_names[u_index]
    v_name = fit.model.exog_names[v_index]


    # Extract parameters  and input parameters of the linear model for tide
    exog_u = fit.model.exog[:, u_index]
    param_u = fit.params[u_name]
    exog_v = fit.model.exog[:, v_index]
    param_v = fit.params[v_name]

    sea_surface_height_due_to_tide = exog_u * param_u + exog_v * param_v
    return sea_surface_height_due_to_tide
