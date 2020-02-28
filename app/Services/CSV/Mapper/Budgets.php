<?php
/**
 * Budgets.php
 * Copyright (c) 2020 james@firefly-iii.org
 *
 * This file is part of the Firefly III CSV importer
 * (https://github.com/firefly-iii/csv-importer).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

namespace App\Services\CSV\Mapper;

use App\Services\FireflyIIIApi\Model\Budget;
use App\Services\FireflyIIIApi\Request\GetBudgetsRequest;

/**
 * Class Budgets
 */
class Budgets implements MapperInterface
{

    /**
     * Get map of objects.
     *
     * @return array
     * @throws \App\Exceptions\ApiHttpException
     */
    public function getMap(): array
    {
        $result   = [];
        $request  = new GetBudgetsRequest;
        $response = $request->get();
        /** @var Budget $budget */
        foreach ($response as $budget) {
            $result[$budget->id] = sprintf('%s', $budget->name);
        }

        return $result;
    }
}
